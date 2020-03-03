from django.contrib import admin
from django import forms

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

from school.models import Semester, Student, TakenCourse, CourseAllocation, Course, Session, PasswordConfigurations, \
    Timetable, ExamTimeTable, Level, Fees, Result, User, SchoolFees, PupilAttendance, SchoolClass, Parent, \
    SchoolDetails, Children


class ScoreAdmin(ImportExportModelAdmin):
    list_display = ['student', 'course', 'ca', 'exam', 'total', 'grade', 'comment', 'semester']


class AllocationAdmin(ImportExportModelAdmin):
    list_display = ['lecturer', ]


class ResultAdmin(ImportExportModelAdmin):
    list_display = ['student', 'gpa', 'semester', 'level', 'cgpa']


class FeesAdmin(ImportExportModelAdmin):
    list_display = ('grade', 'fee')
    list_display_links = ('grade', 'fee')
    list_per_page = 10
    search_fields = ('grade', 'fee')

class TimeTableAdmin(ImportExportModelAdmin):
    list_display = ('course', 'day', 'start_time', 'end_time', 'venue', 'description')
    list_display_links = ('course', 'day', 'start_time', 'end_time', 'venue', 'description')
    list_per_page = 10
    search_fields = ('course__courseTitle', 'day', 'start_time', 'end_time', 'venue', 'description')

class TheUserAdmin(UserAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'address', 'email', 'is_student', 'is_lecturer', 'is_librarian', 'is_parent', 'password_type', 'days_for_password_expiry', 'last_password_reset_date', 'password_expiry_date', 'is_password_expired')
    list_display_links = ('first_name', 'last_name', 'phone', 'address', 'email', 'is_student', 'is_lecturer', 'is_librarian', 'is_parent', 'password_type', 'days_for_password_expiry', 'last_password_reset_date', 'password_expiry_date', 'is_password_expired')
    list_per_page = 10
    search_fields = ('first_name', 'last_name', 'phone', 'address', 'email', 'is_student', 'is_lecturer', 'is_librarian', 'is_parent', 'password_type')


class SchoolFeesAdmin(ImportExportModelAdmin):
    list_display = (
    'student', 'semester', 'gradefees', 'paystatus', 'paymentdate', 'amountpaid', 'actualamountpaid', 'balance',
    'total')
    list_display_links = ('student', 'gradefees', 'paystatus', 'paymentdate', 'amountpaid', 'balance', 'total')
    list_per_page = 10
    search_fields = (
    'student__user__username', 'gradefees__fee', 'paystatus', 'paymentdate', 'amountpaid', 'balance', 'total')


class PupilAttendanceAdmin(ImportExportModelAdmin):
    list_display = ('nameofclass', 'student', 'mark_attendance', 'daysdate', )
    list_display_links = ('nameofclass', 'student', 'mark_attendance', 'daysdate', )
    list_per_page = 10
    search_fields = ('student__user__username', 'mark_attendance', 'daysdate', )
    date_hierarchy = 'daysdate'


class SchoolClassDropDownFields(forms.ModelForm):
    User = get_user_model()
    classteacher = forms.ModelChoiceField(User.objects.filter(is_lecturer=True))

    class Meta:
        model = SchoolClass
        exclude = ('created', )

class SchoolClassAdmin(ImportExportModelAdmin):
    form = SchoolClassDropDownFields
    list_display = ('grade', 'classname', 'classteacher')
    list_display_links = ('grade', 'classname', 'classteacher')
    list_per_page = 10
    search_fields = ('grade', 'classname', 'classteacher')


class ExamTimeTableAdmin(ImportExportModelAdmin):
    list_display = ('course', 'date', 'time', 'venue', 'semester', 'additional_info')
    list_display_links = ('course', 'date', 'time', 'venue', 'semester', 'additional_info')
    list_per_page = 10
    search_fields = ('course', 'date', 'time', 'venue', 'semester', 'additional_info')


class PasswordConfigurationsAdmin(ImportExportModelAdmin):
    list_display = ('user_type', 'number_of_days_to_expire')
    list_display_links = ('user_type', 'number_of_days_to_expire')
    list_per_page = 10
    search_fields = ('user_type', 'number_of_days_to_expire')


class StudentAdmin(ImportExportModelAdmin):
    list_display = ('user', 'id_number', 'schoolclass', 'enrollment_date', 'level')
    list_display_links = ('user', 'id_number', 'schoolclass', 'enrollment_date', 'level')
    list_per_page = 10
    search_fields = ('user', 'id_number', 'schoolclass', 'enrollment_date', 'level')


class ParentsAdmin(ImportExportModelAdmin):
    list_display = ('user', 'occupation', 'nationality')
    list_display_links = ('user', 'occupation', 'nationality')
    list_per_page = 10
    search_fields = ('user', 'occupation', 'nationality')

    # def get_students(self, obj):
    #     return ",".join([s.user.get_full_name() for s in obj.student.all()])


class ChildrenAdmin(ImportExportModelAdmin):
    list_display = ('parent', 'student', 'relation')
    list_display_links = ('parent', 'student', 'relation')
    search_fields = ('parent__user', 'student__user', 'relation')
    autocomplete_fields = ('parent', 'student')
    list_per_page = 10



class LevelAdmin(ImportExportModelAdmin):
    list_display = ('level',)
    list_display_links = ('level',)
    list_per_page = 10
    search_fields = ('level',)


class SchoolDetailsAdmin(ImportExportModelAdmin):
    list_display = ('schoolname', 'address', 'email', 'phone', 'photo')
    list_display_links = ('schoolname', 'address', 'email', 'phone', 'photo')
    list_per_page = 10
    search_fields = ('schoolname', 'address', 'email', 'phone', 'photo')


admin.site.register(SchoolDetails, SchoolDetailsAdmin)
admin.site.register(Semester)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course)
admin.site.register(CourseAllocation, AllocationAdmin)
admin.site.register(TakenCourse, ScoreAdmin)
admin.site.register(Session)
admin.site.register(User, TheUserAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Fees, FeesAdmin)
admin.site.register(SchoolFees, SchoolFeesAdmin)
admin.site.register(PupilAttendance, PupilAttendanceAdmin)
admin.site.register(SchoolClass, SchoolClassAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(ExamTimeTable, ExamTimeTableAdmin)
admin.site.register(Timetable, TimeTableAdmin)
admin.site.register(PasswordConfigurations, PasswordConfigurationsAdmin)
admin.site.register(Parent, ParentsAdmin)
admin.site.register(Children, ChildrenAdmin)
