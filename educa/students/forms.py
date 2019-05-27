from django import forms
from courses.models import Course

#Form สร้างปุ่ม เข้าเรียน เป็น HiddenInput เพราะแสดงปุ่มอย่างเดียว
class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)