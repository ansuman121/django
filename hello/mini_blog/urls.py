from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from mini_blog import views
urlpatterns = [
   path("",views.index , name="home"),
   path("about",views.about , name='about'),
   path("contact",views.contact , name='contact'),
   path('user_login/<str:loc>/',views.user_login , name='user_login'),
   path('signup/<str:loc>/',views.signup , name='signup'),
   path('logout', views.user_logout, name='logout'),
   path('write_blog/<str:loc>/', views.write_blog, name='write_blog'),
   path('ckeditor/', include('ckeditor_uploader.urls')),
   path('show_blogs/', views.show_blogs, name='show_blogs'),
   path('blog_details/<int:pk>/' , views.blog_details , name='blog_details'),
   path('example_blog/', views.example_blog, name='example_blog'),
   path('search/', views.search_blogs, name='search_blog'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)