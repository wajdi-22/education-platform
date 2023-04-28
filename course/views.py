from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import *
from django.db.models import Q


# Create your views here.
def index(request):
    return render(request, 'course/index.html')


# def login(request):
#
#     return None

def dashboard(request):
    return render(request, 'blog.html')


def test_auth(request):
    try:
        teacher = request.user.teacher
        return redirect('teacher')
    except:
        pass
    try:
        student = request.user.student
        return redirect('student')

    except:
        pass
    try:
        parent = request.user.parent
        return redirect('parent')
    except:
        pass
    return redirect('index')


def teacher(request):
    return render(request, 'course/teacher/teacher.html',
                  {'first_name': request.user.first_name, 'full_name': request.user.get_full_name(), 'role': 'Teacher'})
    return HttpResponse(request.user.teacher.__str__())


def student(request):
    return render(request, 'course/student/student.html',
                  {'first_name': request.user.first_name, 'full_name': request.user.get_full_name(), 'role': 'Student'})
    return HttpResponse(request.user.student.__str__())


def parent(request):
    return render(request, 'course/parent/parent.html',
                  {'first_name': request.user.first_name, 'full_name': request.user.get_full_name(),
                   'role': f'parent of {request.user.parent.kid.user.first_name}'})
    return HttpResponse(request.user.parent.__str__())





def list_courses(request):
    subjects = request.user.teacher.subjects.all()
    return render(request, 'course/teacher/list_courses_teacher.html',
                  {'subjects': subjects, 'first_name': request.user.first_name,
                   'full_name': request.user.get_full_name(), 'role': 'Teacher'})
    # return  HttpResponse(request.user.teacher.subjects.all())


def list_chapters(request, level, subject):
    sub = Subject.objects.get(Q(name=subject) & Q(level=Level.objects.get(number=level)))
    chapters = Chapter.objects.filter(subject=sub)
    return render(request, 'course/teacher/list_chapters_teacher.html',
                  {'chapters': chapters, 'subject': sub.__str__(), 'first_name': request.user.first_name,
                   'full_name': request.user.get_full_name(), 'role': 'Teacher'})


def list_course_material(request, level, subject, chapter):
    sub = Subject.objects.get(Q(name=subject) & Q(level=Level.objects.get(number=level)))
    chapterr = Chapter.objects.get(Q(subject=sub) & Q(name=chapter))
    course_material = CourseMaterial.objects.filter(chapter=chapterr)
    # print(course_material)
    return render(request, 'course/teacher/list_course_material_teacher.html',
                  {'course_material': course_material, 'subject': sub, 'chapter': chapterr,
                   'first_name': request.user.first_name,
                   'full_name': request.user.get_full_name(), 'role': 'Teacher'})


def view_course_material(request, level, subject, chapter, slug):
    course_material = CourseMaterial.objects.get(slug=slug)
    audiofile=course_material.audio.url
    audiofile=audiofile.replace('course/static/','')
    summaries_audio=course_material.summary_audio.url
    summaries_audio = summaries_audio.replace('course/static/', '')
    sub = Subject.objects.get(Q(name=subject) & Q(level=Level.objects.get(number=level)))
    chapterr = Chapter.objects.get(Q(subject=sub) & Q(name=chapter))
    return render(request, 'course/teacher/view_course_material_teacher.html',
                  {'course_material': course_material,'summaries_audio':summaries_audio,'audiofile':audiofile, 'subject': sub, 'chapter': chapterr,
                   'first_name': request.user.first_name,
                   'full_name': request.user.get_full_name(), 'role': 'Teacher'})


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
            return render(request, 'add_course_material.html',
                          {'errors': errors, 'title': title, 'content': content, 'summary': summary})

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
        return render(request, 'course/teacher/add_course_material_teacher.html',{'first_name': request.user.first_name,
                                                                                  'full_name': request.user.get_full_name(), 'role': 'Teacher'})



