from django.shortcuts import render , redirect 
from taskmanager.models import tasks
from django.contrib import messages
# Create your views here.
def view_task(request):
    post = tasks.objects.all()
    return render(request , 'view_task.html' , {"posts" : post})

def add_task(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        task = request.POST.get('task')
        if task == "" and name == "" :
            messages.warning(request, "enter the following fields")
        else:
            data = tasks(name= name , task = task)
            data.save()
            messages.success(request,"task added sucessfully")
    return render(request , 'task.html')
    
def delete_task(request , id):
    task = tasks.objects.get(id = id)
    task.delete()
    return redirect("/")
def completed_task(request , id):
    task = tasks.objects.get(id = id)
    task.completed = True
    task.save()
    return redirect("/")