from django.shortcuts import render

# ชุด import ระบบสมาชิกนักเรียน
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

# ชุด import สำหรับเข้าร่วมคอร์สเรียน
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm

# ชุด import สำหรับแสดง course contents เมื่อนักเรียนเข้าร่วมคอร์สนั้นแล้ว
from django.views.generic.list import ListView
from courses.models import Course

#ชุด import สำหรับอธิบายรายละเอียดคอร์สเรียน
from django.views.generic.detail import DetailView

#View แบบฟอร์มสมัครสมาชิกนักเรียน
class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super(StudentRegistrationView,
                        self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return result

#View แบบฟอร์มปุ่มกดเข้าร่วมเรียน
class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView,
                self).form_valid(form)
                
    def get_success_url(self):
        return reverse_lazy('student_course_detail',
                            args=[self.course.id])

#ListView แสดงคอร์สทั้งหมดที่นักเรียนคนนั้นเข้าร่วมเรียน
class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

#View แสดงรายละเอียดของคอร์ส
class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super(StudentCourseDetailView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(StudentCourseDetailView,
                        self).get_context_data(**kwargs)
    # get course object
    course = self.get_object()
    if 'module_id' in self.kwargs:
        # get current module
        context['module'] = course.modules.get(
                                id=self.kwargs['module_id'])
    else:
        # get first module
        context['module'] = course.modules.all()[0]
    return context