from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import icoder , Contacts , BlogPost
from django.http import JsonResponse
from .forms import BlogPostForm
# Create your views here.
def signup(request , loc):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm_password']
        confirmation = request.POST.get("confirm") == 'on'
        if confirmation:
            if password != confirm:
                messages.warning(request , "password do not match")
                return redirect(loc)
            
            if icoder.objects.filter(email=email).exists():
                messages.warning(request, "Email already registered!")
                return redirect('home')
            
            if icoder.objects.filter(name=name).exists():
                messages.warning(request, "Username already exists!")
                return redirect(loc) 
            
            user = icoder(name=name , email=email , password=password)
            user.save()
            messages.success(request , "account has been created")
        else:
            messages.warning(request , "please check the confirmation")
        return redirect(loc)
    

def user_login(request, loc):
    if request.method == "POST":
        email = request.POST['l_email']
        password = request.POST['l_pass']
        confirm = request.POST.get("l_confirm") == 'on'

        if not confirm:
            messages.warning(request, "Please check the confirmation box.")
            return redirect(loc)

        try:
            user = icoder.objects.get(email=email)
        except icoder.DoesNotExist:
            messages.warning(request, "Email not registered!")
            return redirect(loc)

        if user.password != password:
            messages.error(request, "Incorrect password!")
            return redirect(loc)

        
        request.session['user_id'] = user.id
        request.session['user_name'] = user.name
        messages.success(request, "Logged in successfully!")
        return redirect(loc) 

    return redirect(loc)

def index(request):
    
    return render(request , 'index_new.html')

def about(request):
    return render(request , 'about.html')

def contact(request):
    if request.method == "POST":
        email = request.POST['email']
        domain = request.POST['domain']
        member = request.POST.get("member") == 'on'
        coder = request.POST.get("coder") == 'on'
        proffesor = request.POST.get("proffessor") == 'on'
        about_yourself = request.POST['about_yourself']
        query = request.POST['query']

        try:
            check = icoder.objects.get(email=email)
        except icoder.DoesNotExist:
            messages.warning(request, "Email not registered!")
            return redirect('contact')
        
        user = Contacts(email=email , domain = domain , member = member , coder = coder , proffesor = proffesor , about_yourself = about_yourself , query = query)
        user.save()
        messages.success(request , "issue has been raised")

    return render(request , 'contact.html')

def user_logout(request):
    try:
        del request.session['user_id']
        del request.session['user_name']
    except KeyError:
        pass
    messages.success(request, "Logged out successfully!")
    return redirect('home')

def write_blog(request, loc):
    if 'user_id' not in request.session:
        messages.warning(request, "Please log in to write a blog")
        return redirect('user_login', loc=loc)

    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            
            user_id = request.session.get('user_id')
            try:
                user = icoder.objects.get(id=user_id)
            except icoder.DoesNotExist:
                messages.warning(request, "User not found. Please log in again.")
                return redirect('user_login', loc=loc)

            blog.author = user
            blog.save()
            messages.success(request, "Blog posted successfully!")
            return redirect('home')
    else:
        form = BlogPostForm()

    return render(request, 'write_blog.html', {'form': form})

def show_blogs(request ):
    
    selected_domain = request.GET.get('domain')
    if selected_domain:
        blogs = BlogPost.objects.filter(domain=selected_domain).order_by('-date_posted')
    else:
        blogs = BlogPost.objects.all().order_by('-date_posted')

    domains = BlogPost.objects.values_list('domain', flat=True).distinct()

    return render(request, 'all_blogs.html', {
        'blogs': blogs,
        'domains': domains,
        'selected_domain': selected_domain
    })

def blog_details(request , pk ):
    blog = get_object_or_404(BlogPost , pk = pk)
    return render(request , 'blog_details.html' , {'blog' : blog})

def example_blog(request):
    return render(request , 'blog_example.html')


def search_blogs(request):
    query = request.GET.get('q')
    blogs = BlogPost.objects.filter(title__icontains=query)
    results = [{'id': blog.pk, 'title': blog.title} for blog in blogs]
    return JsonResponse(results, safe=False)








