from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import *






# Create your views here.
def index(request):
    return render(request, 'course/index.html')


# def login(request):
#
#     return None

def dashboard(request):
    return render(request,'blog.html')

def test_auth(request):
    try:
        teacher=request.user.teacher
        return redirect('teacher')
    except:
        pass
    try:
        student=request.user.student
        return redirect('student')

    except:
        pass
    try:
        parent=request.user.parent
        return redirect('parent')
    except:
        pass
    return redirect('index')


def teacher(request):
    return HttpResponse(request.user.teacher.__str__())


def student(request):
    return HttpResponse(request.user.student.__str__())


def parent(request):
    return HttpResponse(request.user.parent.__str__())


def posts_page(request):
    return render(request, 'blog.html')


def post_detail_page(request, slug):
    return render(request, 'post_detail_page.html', {'slug': slug})



@csrf_exempt
def add_course_material(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        summary = request.POST.get('summary')
        chapter_id = request.POST.get('chapter')
        subject_id = request.POST.get('subject')

        # Generate summary if not provided
        if not summary:
            summary = 'bbbbmmmmmmmmmlllamammammamamammammamamamma'

        # Validate inputs
        errors = {}

        if not title:
            errors['title'] = 'Title is required.'

        if not content:
            errors['content'] = 'Content is required.'

        if not chapter_id:
            errors['chapter'] = 'Chapter is required.'

        if not subject_id:
            errors['subject'] = 'Subject is required.'

        if errors:
            return render(request, 'add_course_material.html', {'errors': errors, 'title': title, 'content': content, 'summary': summary})

        # Create new course material
        chapter = Chapter.objects.get(pk=chapter_id)
        subject = Subject.objects.get(pk=subject_id)

        course_material = CourseMaterial.objects.create(
            title=title,
            content=content,
            summary=summary,
            chapter=chapter,
            subject=subject
        )

        # Redirect to course material detail page
        return redirect('course_material_detail', pk=course_material.pk)

    else:
        return render(request, 'add_course_material.html')







