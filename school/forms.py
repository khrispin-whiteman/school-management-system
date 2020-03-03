from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import *
from django.forms import BaseModelFormSet


PARENT_CHILD_RELATION = (
    ("Father", "Father"),
    ("Mother", "Mother"),
    ("Brother", "Brother"),
    ("Sister", "Sister"),
    ("Uncle", "Uncle"),
    ("Aunty", "Aunty"),
    ("Cousin", "Cousin"),
    ("Grand-Parent", "Grand-Parent"),
    ("Other", "Other"),
)


class StaffAddForm(UserCreationForm):
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Mobile No.",
    )

    firstname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Firstname",
    )

    lastname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Lastname",
    )

    email = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Email",
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_lecturer = True
        user.first_name = self.cleaned_data.get('firstname')
        user.last_name = self.cleaned_data.get('lastname')
        user.phone = self.cleaned_data.get('phone')
        user.address = self.cleaned_data.get('address')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class ParentAddForm(UserCreationForm):
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Mobile No.",
    )

    firstname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Firstname",
    )

    lastname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Lastname",
    )

    email = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Email",
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_parent = True
        user.first_name = self.cleaned_data.get('firstname')
        user.last_name = self.cleaned_data.get('lastname')
        user.phone = self.cleaned_data.get('phone')
        user.address = self.cleaned_data.get('address')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class ParentChildrenAddForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=Parent.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Parent',
    )
    student = forms.ModelChoiceField(
        queryset=Student.objects.filter().order_by('level'),
        #queryset=User.objects.filter(is_student=True),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Student',
    )

    relation = forms.CharField(
        widget=forms.Select(
            choices=PARENT_CHILD_RELATION,
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        label="semester",
    )


    class Meta:
        model = Children
        fields = ['student', 'parent', 'relation', ]

    # @transaction.atomic()
    # def save(self, commit=True,):
    #     parent = super().save(commit=False)
    #     print('FIRST PRINT USER ID: ', self.cleaned_data.get('parent'))
    #     #paruser = User.objects.get(id=self.cleaned_data.get('parent'))
    #     print('SECOND PRINT USER ID: ', self.cleaned_data.get('parent'))
    #
    #     parent.user = self.cleaned_data.get('parent')
    #
    #     if commit:
    #         parent.save()
    #     return parent


class StudentAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Username",
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Mobile No.",
    )

    firstname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Firstname",
    )

    lastname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Lastname",
    )

    level = forms.ModelChoiceField(queryset=Level.objects.all(),
                                   widget=forms.Select(
                                       attrs={'class': 'btn-block', 'style': 'height: 40px;'}),
                                   empty_label='Choose Level')

    schoolclass = forms.ModelChoiceField(queryset=SchoolClass.objects.all(),
                                   widget=forms.Select(
                                       attrs={'class': 'btn-block', 'style': 'height: 40px;'}),
                                   empty_label='Choose Class')

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
            }
        ),
        label="Email Address",
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('firstname')
        user.last_name = self.cleaned_data.get('lastname')
        user.phone = self.cleaned_data.get('phone')
        user.email = self.cleaned_data.get('email')
        user.save()
        student = Student.objects.create(user=user, id_number=user.username, level=self.cleaned_data.get('level'), schoolclass=self.cleaned_data.get('schoolclass'))

        # get_class = SchoolClass.objects.get(classname__exact=self.cleaned_data.get('schoolclass'))

        student.save()

        get_class = SchoolClass.objects.get(id=student.schoolclass.id)
        for c in get_class.courses.all():
            taken_course = TakenCourse.objects.create(student=student, semester=c.semester, course=c)
            taken_course.save()
            print("THE CLASS: ", c)

        #print("CLASS NAME: ", get_class.classname)
        return user


class SchoolClassAddForm(forms.ModelForm):
    grade = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Grade',
    )

    classname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Class Name",
    )

    classteacher = forms.ModelChoiceField(
        queryset=User.objects.filter(is_lecturer=True),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Class Teacher',
    )

    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.filter(semester__is_current_semester=True),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


    class Meta:
        model = SchoolClass
        fields = ['grade', 'classname', 'classteacher', 'courses']


class SchoolClassEditForm(forms.ModelForm):
    grade = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Grade',
    )

    classname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Class Name",
    )

    classteacher = forms.ModelChoiceField(
        queryset=User.objects.filter(is_lecturer=True),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Class Teacher',
    )

    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.filter(semester__is_current_semester=True),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


    class Meta:
        model = SchoolClass
        fields = ['grade', 'classname', 'classteacher', 'courses']


class StudentCourseRegistrationForm(forms.ModelForm):
    semester = forms.ModelChoiceField(
        queryset=Semester.objects.filter(is_current_semester=True),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Semester',
    )
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Student',
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(semester__is_current_semester=True),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Course',
    )

    class Meta:
        model = TakenCourse
        fields = ['student', 'course', 'semester']

    # def save(self):
    #     student = super().save(commit=False)
    #     student.semester = Semester.objects.get(is_current_semester=True)
    #     return student


class ClassTimetableForm(forms.ModelForm):
    semester = forms.ModelChoiceField(
        queryset=Semester.objects.filter(is_current_semester=True),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Semester',
    )
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Student',
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(semester__is_current_semester=True),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Course',
    )

    class Meta:
        model = TakenCourse
        fields = ['student', 'course', 'semester']


class FeesStructureAddForm(forms.ModelForm):
    grade = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Grade',
    )


    fee = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Amount",
    )


    class Meta:
        model = Fees
        fields = ['grade', 'fee',]


class FeesCollectionForm(forms.ModelForm):
    semester = forms.ModelChoiceField(
        queryset=Semester.objects.filter(is_current_semester=True),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Term',
    )
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Student',
    )
    gradefees = forms.ModelChoiceField(
        queryset=Fees.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Fees Structure',
    )

    amountpaid = forms.DecimalField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label="*Amount Paid",
    )

    class Meta:
        model = SchoolFees
        fields = ['semester', 'student', 'gradefees', 'amountpaid']


class CourseAddForm(forms.ModelForm):
    courseTitle = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label="*Course Title",
    )

    courseCode = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label="*Course Code",
    )

    courseUnit = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label="*Course Unit",
    )

    description = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        label="Add a little description",
        required=False,
    )

    level = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Grade',
    )

    semester = forms.ModelChoiceField(
        queryset=Semester.objects.all(),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        empty_label='Choose Term',
    )

    is_elective = forms.BooleanField(label="*is_elective", required=False)

    class Meta:
        model = Course
        fields = ['courseCode', 'courseTitle', 'courseUnit', 'level', 'description', 'semester', 'is_elective']


class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Old password",
        required=True)

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New password",
        required=True)
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm new password",
        required=True)

    class Meta:
        model = User
        fields = ['id', 'password', 'password1', 'password2']

    def clean(self):
        super(ChangePasswordForm, self).clean()
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        id = self.cleaned_data.get('id')
        user = User.objects.get(pk=id)
        if not user.check_password(password):
            self._errors['password'] = self.error_class([
                'Old password don\'t match'])
        if password1 and password1 != password2:
            self._errors['password1'] = self.error_class([
                'Passwords don\'t match'])
        return self.cleaned_data


class CourseAllocationForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.filter(semester__is_current_semester=True).order_by('level'),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    lecturer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_lecturer=True),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        label="teacher",
    )

    class Meta:
        model = CourseAllocation
        fields = ['lecturer', 'courses']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CourseAllocationForm, self).__init__(*args, **kwargs)
        self.fields['lecturer'].queryset = User.objects.filter(is_lecturer=True)


class CourseRegitsrationForm(forms.ModelForm):
    class Meta:
        model = TakenCourse
        fields = ('course',)
        widgets = {
            'course': forms.CheckboxSelectMultiple
        }


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Firstname",
        max_length=30,
        required=False)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Lastname",
        max_length=30,
        required=False)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Email",
        max_length=75,
        required=False)
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Phone Number",
        max_length=16,
        required=False)

    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Home Address",
        max_length=200,
        required=False)

    picture = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Upload picture",
        required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'phone', 'address', 'picture']


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['session']


class SemesterForm(forms.ModelForm):
    semester = forms.CharField(
        widget=forms.Select(
            choices=SEMESTER,
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        label="semester",
    )
    is_current_semester = forms.CharField(
        widget=forms.Select(
            choices=((True, 'Yes'), (False, 'No')),
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        label="is current semester ?",
    )
    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        required=True
    )

    next_semester_begins = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'type': 'date',
            }
        ),
        required=True)

    class Meta:
        model = Semester
        fields = ['semester', 'is_current_semester', 'session', 'next_semester_begins']


class_attendance = (
    ('Present', 'Present'),
    ('Absent', 'Absent'),
)


class StudentAttendanceForm(forms.Form):
    mark_attendance = forms.ChoiceField(widget=forms.RadioSelect, initial=class_attendance[0], choices=class_attendance)