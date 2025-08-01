from django.shortcuts import render ,redirect , HttpResponse
from home.models import blog_post
from django.contrib import messages
# Create your views here.
def postblogs(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title == "" or content == "":
            messages.warning(request,"enter valid details")
        else:
            blog = blog_post(title= title , content= content)
            blog.save()
            messages.success(request , "blog successfully uploaded...")
        return redirect("/")
    
    return render(request, 'blog.html')
def displayblogs(request):

    posts = blog_post.objects.all()
    return render(request, 'view.html', {'posts': posts})
    
