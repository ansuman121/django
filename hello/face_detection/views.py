from django.shortcuts import render , redirect
from django.contrib import messages
import cv2 , os
import face_recognition ,time
from sklearn import neighbors
import pickle
import warnings 
import numpy as np
from django.http import JsonResponse , StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
warnings.filterwarnings("ignore", category=UserWarning)
# Create your views here
import threading
import traceback

camera = None
frame_lock = threading.Lock()
latest_frame = None
camera_running = False
test_runner = None
flag = True
KNOW_FOLDER = "/Users/ansumanpattanaik/Downloads/archive"
class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.running = True
        self.thread = threading.Thread(target=self.update_frame, daemon=True)
        self.thread.start()
        self.frame = None
        self.face_locations = None

    def update_frame(self):
        global latest_frame
        while self.running:
            success, frame = self.video.read()
            if success:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                face_locations = face_recognition.face_locations(small_frame)
                if len(face_locations) > 0:
                    for (top, right, bottom, left) in face_locations:
                        top *= 4
                        right *= 4
                        bottom *= 4
                        left *= 4
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                ret, buffer = cv2.imencode('.jpg', frame)
                self.frame = small_frame
                self.face_locations = face_locations
                with frame_lock:
                    latest_frame = buffer.tobytes()
            time.sleep(0.03)

    def stop(self):
        self.running = False
        time.sleep(0.1)
        self.video.release()


def generate_frames():
    global latest_frame

    while True:
        with frame_lock:
            if latest_frame is not None:
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')

        time.sleep(0.03)
@csrf_exempt
def start_camera(request):
    global camera, camera_running
    if request.method == 'POST':
        if not camera_running:
            camera = VideoCamera()
            camera_running = True
        return JsonResponse({"message": "Camera started successfully!"})

@csrf_exempt
def stop_camera(request):
    global camera, camera_running ,flag
    if request.method == 'POST' and camera_running:
        camera.stop()
        camera = None
        camera_running = False
        flag = False
        return JsonResponse({"message": "Camera stopped successfully!"})   
    else:
        return JsonResponse({"message": "Camera is not running."}) 
     
def index(request):
    return render(request , "face.html")


def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


@csrf_exempt
def train_model_view(request):
    if request.method == 'POST':
        train_model(request)  # call the helper
        return JsonResponse({"message": "Training completed successfully!"})
    return JsonResponse({"error": "Invalid request"}, status=400)
def train_model(request ,model_save_path="knn_model.clf", n_neighbors=2):
    print("🚀 train_model function is called")
    folder = KNOW_FOLDER
    x , y = [] , []
    for person_name in os.listdir(folder):
        person_path = os.path.join(folder , person_name) 
        if not os.path.isdir(person_path):
            continue
        for image_name in os.listdir(person_path):
            image_path = os.path.join(person_path , image_name)
            image = face_recognition.load_image_file(image_path)
            image_loc = face_recognition.face_locations(image)

            if len(image_loc) != 1:
                messages.warning(request , f"Image {image_path} not suitable for training: Found {len(image_loc)} faces.")
                continue            
            face_encoding = face_recognition.face_encodings(image , known_face_locations= image_loc)[0]
            x.append(face_encoding)
            y.append(person_name)

    knn_clf = neighbors.KNeighborsClassifier(n_neighbors= n_neighbors , algorithm="ball_tree" , weights="distance")
    knn_clf.fit(x,y)

    with open(model_save_path , "wb") as f :
        pickle.dump(knn_clf,f)
    print("successfully trained")
class TestRunner:
    def __init__(self, camera_obj):
        self.camera = camera_obj
        self.running = True
        self.results = []
        self.thread = threading.Thread(target=self.test_loop, daemon=True)
        self.thread.start()

    def test_loop(self):
        while self.running:
            if self.camera.frame is not None and self.camera.face_locations:
                try:
                    res = self.predict(self.camera.face_locations, self.camera.frame)
                    self.results = res
                except Exception as e:
                    print("Prediction error:", e)
            time.sleep(1)  # Run prediction every 1 second

    def predict(self, face_locations, frame):
        with open("knn_model.clf", "rb") as f:
            knn_clf = pickle.load(f)

        encodings = face_recognition.face_encodings(frame, known_face_locations=face_locations)
        if not encodings:
            return []

        closest_distances = knn_clf.kneighbors(encodings, n_neighbors=1)
        are_matches = [dist[0] <= 0.6 for dist in closest_distances[0]]

        predictions = []
        for pred, loc, match in zip(knn_clf.predict(encodings), face_locations, are_matches):
            name = pred if match else "Unknown"
            predictions.append([name, loc])

        return predictions

    def stop(self):
        self.running = False

@csrf_exempt
def start_testing(request):
    global test_runner, camera

    if request.method == 'POST':
        if not camera or not camera_running:
            return JsonResponse({"error": "Camera not running"}, status=400)

        if test_runner is None:
            test_runner = TestRunner(camera)
            return JsonResponse({"message": "Testing started in background"})
        else:
            return JsonResponse({"message": "Testing already running"})
        
@csrf_exempt
def stop_testing(request):
    global test_runner

    if request.method == 'POST':
        if test_runner:
            test_runner.stop()
            test_runner = None
            return JsonResponse({"message": "Testing stopped"})
        return JsonResponse({"message": "Testing not running"})    
@csrf_exempt
def get_results(request):
    global test_runner

    if test_runner:
        return JsonResponse({"results": [{"name": r[0]} for r in test_runner.results]})
    return JsonResponse({"results": []})    

    
