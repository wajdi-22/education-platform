from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path('blog/',views.posts_page),
    path("blog/<slug:slug>",views.post_detail_page),
    path("add/",views.add_course_material)

]