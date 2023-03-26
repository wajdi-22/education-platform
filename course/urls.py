from django.urls import path
from . import views

urlpatterns = [
    path("", views.index,name='index'),
    path('test_auth', views.test_auth),
    path('blog/',views.posts_page),
    path("blog/<slug:slug>",views.post_detail_page),
    path("add/",views.add_course_material)

]