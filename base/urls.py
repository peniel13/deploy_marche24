from django.urls import path
from .import views

urlpatterns= [
    path('',views.index, name= 'index'),
    path('list_product/',views.list_product, name= 'list_product'),
    path('list_store/',views.list_store, name= 'list_store'),
    path('contact/', views.contact, name='contact'),
    path('apropos/', views.apropos, name='apropos'),
    path('politique/', views.politique, name='politique'),
    path('videos/', views.video_list, name='video_list'),
    path('fetch_video/<slug:slug>/', views.fetch_video, name='fetch_video'),
    path('video-pub/<slug:slug>/', views.fetch_video_pub, name='fetch_video_pub'),
    path('publicites/', views.publicite_video_list, name='publicite_video_list'),
]