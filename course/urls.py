from django.urls import path
from . import views

urlpatterns = [
    path("", views.index,name='index'),
    path("teacher/",views.teacher,name='teacher'),
    path("teacher/courses",views.list_courses,name='list_courses'),
    path("teacher/courses/<int:level>/<str:subject>",views.list_chapters,name='list_chpters'),
    path("teacher/courses/<int:level>/<str:subject>/<str:chapter>",views.list_course_material,name='list_course_material'),
    path("teacher/courses/<int:level>/<str:subject>/<str:chapter>/<slug:slug>",views.view_course_material,name='view_course_material'),
    path("teacher/course/add",views.add_course_material,name='add_course_material'),

    path("student/",views.student,name='student'),
    path("parent/",views.parent,name='parent'),
    path('test_auth', views.test_auth),


]