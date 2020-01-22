import decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.urls import reverse

from school.validators import ASCIIUsernameValidator

A = "A"
B = "B"
C = "C"
D = "D"
F = "F"
PASS = "PASS"
FAIL = "FAIL"

GRADE = (
    (A, 'A'),
    (B, 'B'),
    (C, 'C'),
    (D, 'D'),
    (F, 'F'),
)

COMMENT = (
    (PASS, "PASS"),
    (FAIL, "FAIL"),
)

LEVEL = (
    ("1", 1),
    ("2", 2),
    ("3", 3),
    ("4", 4),
    ("5", 5),
)
FIRST = "First"
SECOND = "Second"
THIRD = "Third"

SEMESTER = (
    (FIRST, "First"),
    (SECOND, "Second"),
    (THIRD, "Third"),
)

PASSWORD_TYPES = (
    ('Expirable', 'Expirable'),
    ('None-Expirable', 'None-Expirable'),
)

class_attendance = (
    ('Present','Present'),
    ('Absent','Absent'),
)

class PasswordConfigurations(models.Model):
    user_type = models.CharField('User Type', help_text='e.g Student', max_length=200, default='All Users')
    number_of_days_to_expire = models.IntegerField('Days', default=30)

    class Meta:
        verbose_name = 'Password Configuration'
        verbose_name_plural = 'Password Configurations'


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    phone = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    picture = models.ImageField(upload_to="users/pictures/%Y/%m/%d'", blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    #password settings
    password_type = models.CharField('Password Type', default='Expirable', max_length=200, choices=PASSWORD_TYPES)
    days_for_password_expiry = models.ForeignKey(PasswordConfigurations, on_delete=models.CASCADE, null=True, blank=True)
    last_password_reset_date = models.DateField('Reset On', auto_now=True)
    password_expiry_date = models.DateField(editable=False, null=True, blank=True)
    is_password_expired = models.BooleanField(default=False,)

    username_validator = ASCIIUsernameValidator()

    def get_picture(self):
        no_picture = settings.STATIC_URL + 'img/img_avatar.png'
        try:
            return self.picture.url
        except:
            return no_picture

    def get_full_name(self):
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name

    def __str__(self):
        return self.get_full_name()

    # def save(self, **kwargs):
    #     from datetime import datetime, timedelta
    #     d = timedelta(days=self.days_for_password_expiry.number_of_days_to_expire + 0)
    #
    #     if self.password_type == 'Expirable':
    #         self.password_expiry_date = datetime.now() + d
    #
    #         # actualprice = self.subscription.price
    #         # self.balance = actualprice - self.paid
    #         #
    #         # if self.balance > 0:
    #         #     self.paystatus = 'you have a balance'
    #
    #         # activate the user upon subscription
    #         # u = User.objects.get(pk=self.user.pk)
    #         # u.is_active = True
    #         # u.save(force_update=u.is_active)
    #         super(User, self).save()


class SystemSettings(models.Model):
    allow_exam_marking = models.BooleanField(default=False)
    exam_start_marking_date = models.DateField(null=True)
    exam_start_marking_date = models.DateField(null=True)

    def __str__(self):
        return self.allow_exam_marking


class Department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Session(models.Model):
    session = models.CharField(max_length=200, unique=True)
    is_current_session = models.BooleanField(default=False, blank=True, null=True)
    next_session_begins = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.session


class Semester(models.Model):
    semester = models.CharField(max_length=10, choices=SEMESTER, blank=True)
    is_current_semester = models.BooleanField(default=False, blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
    next_semester_begins = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.session) + ' - ' + str(self.semester)


class Level(models.Model):
    level = models.CharField('Grade', max_length=200, )

    def __str__(self):
        return self.level

    class Meta:
        verbose_name_plural = 'Levels/Grades'
        verbose_name = 'Level/Grade'


class Course(models.Model):
    courseTitle = models.CharField(max_length=200)
    courseCode = models.CharField(max_length=200, unique=True)
    #courseUnit = models.CharField(max_length=200)
    description = models.TextField(max_length=200, blank=True)
    level = models.ForeignKey(Level, verbose_name='Grade', default='', on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    is_elective = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.courseCode + " (" + self.courseTitle + "), Grade: " + str(self.level)

    def get_absolute_url(self):
        return reverse('course_list', kwargs={'pk': self.pk})

    def get_total_unit(self):
        t = 0
        total = Course.objects.all()
        for i in total:
            t += i
        return i


class SchoolClass(models.Model):
    grade = models.ForeignKey(Level, verbose_name='Level', default='', on_delete=models.CASCADE)
    classname = models.CharField('Enter Class Title', max_length=200, default='', help_text='name of class, (eg. A)')
    classteacher = models.ForeignKey(User, verbose_name='Assign Teacher', max_length=200, default='',
                                     on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, verbose_name='Choose Courses', related_name='class_subject',
                                      help_text='Hold Ctrl to choose multiple')

    def __str__(self):
        return 'Grade: ' + str(self.grade) + self.classname + ', Teacher: ' + str(self.classteacher)

    class Meta:
        verbose_name = 'School Class'
        verbose_name_plural = 'School Classes'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=20, unique=True)
    schoolclass = models.ForeignKey(SchoolClass, verbose_name='Class', default='', on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True, null=True, blank=True)
    level = models.ForeignKey(Level, verbose_name='Grade', default='', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name() + ', Grade: ' + str(self.level)

    def get_absolute_url(self):
        return reverse('profile')


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student, )
    occupation = models.CharField('Occupation', max_length=200, null=True, blank=True)
    nationality = models.CharField('Nationality', max_length=200, null=True, blank=True)

    def get_students(self):
        return ",".join([s.user.get_full_name() for s in self.student.all()])

    def __str__(self):
        return self.user.username

    def save(self, **kwargs):
        if not self.id:
            user = User.objects.get(id=self.user.id)
            user.is_parent = True
            user.save()



class TakenCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, null=True, blank=True, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='taken_courses')
    ca = models.PositiveIntegerField(blank=True, null=True, default=0)
    exam = models.PositiveIntegerField(blank=True, null=True, default=0)
    total = models.PositiveIntegerField(blank=True, null=True, default=0)
    grade = models.CharField(choices=GRADE, max_length=1, blank=True)
    comment = models.CharField(choices=COMMENT, max_length=200, blank=True)

    def get_absolute_url(self):
        return reverse('update_score', kwargs={'pk': self.pk})

    def get_total(self, ca, exam):
        return int(ca) + int(exam)

    def get_grade(self, ca, exam):
        total = int(ca) + int(exam)
        if total >= 70:
            grade = A
        elif total >= 60:
            grade = B
        elif total >= 50:
            grade = C
        elif total >= 45:
            grade = D
        else:
            grade = F
        return grade

    def get_comment(self, grade):
        if not grade == "F":
            comment = PASS
        else:
            comment = FAIL
        return comment


    def calculate_gpa(self, total_unit_in_semester):
        current_semester = Semester.objects.get(is_current_semester=True)
        student = TakenCourse.objects.filter(student=self.student, course__level=self.student.level,
                                             course__semester=current_semester)
        p = 0
        point = 0
        for i in student:
            courseUnit = i.course.courseUnit
            if i.grade == A:
                point = 5
            elif i.grade == B:
                point = 4
            elif i.grade == C:
                point = 3
            elif i.grade == D:
                point = 2
            else:
                point = 0
            p += int(courseUnit) * point
        try:
            gpa = (p / total_unit_in_semester)
            return round(gpa, 1)
        except ZeroDivisionError:
            return 0

    def calculate_cgpa(self):
        current_semester = Semester.objects.get(is_current_semester=True)
        previousResult = Result.objects.filter(student__id=self.student.id, level__lt=self.student.level)
        previousCGPA = 0
        for i in previousResult:
            if i.cgpa is not None:
                previousCGPA += i.cgpa
        cgpa = 0
        if str(current_semester) == SECOND:
            try:
                first_sem_gpa = Result.objects.get(student=self.student.id, semester=FIRST, level=self.student.level)
                first_sem_gpa += first_sem_gpa.gpa.gpa
            except:
                first_sem_gpa = 0

            try:
                sec_sem_gpa = Result.objects.get(student=self.student.id, semester=SECOND, level=self.student.level)
                sec_sem_gpa += sec_sem_gpa.gpa
            except:
                sec_sem_gpa = 0

            taken_courses = TakenCourse.objects.filter(student=self.student, student__level=self.student.level)
            TCU = 0
            for i in taken_courses:
                TCU += int(i.course.courseUnit)
            cpga = first_sem_gpa + sec_sem_gpa / TCU

            return round(cgpa, 2)


class ExamTimeTable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200, blank=True, null=True)
    semester = models.ForeignKey(Semester,  on_delete=models.CASCADE)
    additional_info = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return str(self.course) + ', ' + str(self.venue) + ', ' + str(self.date)


class CourseAllocation(models.Model):
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, related_name='allocated_course')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.lecturer.username


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    gpa = models.FloatField(null=True)
    cgpa = models.FloatField(null=True)
    semester = models.CharField(max_length=100, choices=SEMESTER)
    session = models.CharField(max_length=100, blank=True, null=True)
    level = models.ForeignKey(Level, verbose_name='Level', default='', on_delete=models.CASCADE)


class Fees(models.Model):
    grade = models.ForeignKey(Level, verbose_name='Level', default='', on_delete=models.CASCADE)
    fee = models.DecimalField(verbose_name='Fee To Be Paid', max_digits=20, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Fee Structure'
        verbose_name_plural = 'Fees Structure'

    def __str__(self):
        return 'Grade: ' + str(self.grade) + ' Fees: ' + str(self.fee)


class SchoolFees(models.Model):
    semester = models.ForeignKey(Semester, default='', blank=True, null=True,
                                 verbose_name='Choose Academic Term', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name='Choose Student', null=True, blank=True, on_delete=models.CASCADE)
    gradefees = models.ForeignKey(Fees, verbose_name='Choose Fees Structure', null=True, blank=True,
                                  on_delete=models.CASCADE)
    amountpaid = models.DecimalField(verbose_name='Total Amount Paid', max_digits=20, decimal_places=2, default=0)
    actualamountpaid = models.DecimalField(verbose_name='Actual Amount Paid', max_digits=20, decimal_places=2,
                                           default=0, editable=False)
    balance = models.DecimalField(verbose_name='Balance', max_digits=20, decimal_places=2, default=0, editable=False)
    paystatus = models.CharField(max_length=30, default='Fully Paid', blank=True, null=True, editable=False)
    paymentdate = models.DateField('Paid On', auto_now=True)
    total = models.DecimalField('Fees To Be Paid', max_digits=20, decimal_places=2, default=0, editable=False)

    class Meta:
        verbose_name = 'School Fees'
        verbose_name_plural = 'School Fees'

    def save(self, **kwargs):

        if not self.id:
            fees = SchoolFees.objects.filter(student__user_id=self.student.user.id).order_by('-id')[:1]
            actualfees = self.gradefees.fee
            self.actualamountpaid = self.amountpaid
            amountEntered = decimal.Decimal(self.amountpaid)

            if fees:

                for f in fees:
                    print("")
                    print("SESSION: ", f.semester, "TOTAL: ", f.total, ", PAID: ", f.amountpaid)

                    # check if student over paid
                    if f.semester != self.semester and f.balance < 0:
                        print("FIRST IF STATEMENT:::::")
                        self.amountpaid = decimal.Decimal(self.amountpaid) + (f.amountpaid - f.total)
                        paid = self.amountpaid
                        self.balance = actualfees - paid
                        self.total = actualfees

                    # check if student under paid
                    if f.semester != self.semester and f.balance >= 0:
                        print("SECOND IF STATEMENT:::::")
                        self.amountpaid = decimal.Decimal(self.amountpaid) - f.balance
                        paid = decimal.Decimal(self.amountpaid)
                        self.balance = actualfees - paid
                        self.total = actualfees

                    # if f.academicsession == self.academicsession and actualfees > f.amountpaid > 0:
                    #     print("THIRD IF STATEMENT:::::")
                    #     self.amountpaid = decimal.Decimal(self.amountpaid) + f.amountpaid
                    #     paid = decimal.Decimal(self.amountpaid)
                    #     self.balance = actualfees - paid
                    #     self.total = actualfees

                    if f.semester == self.semester and f.balance >= 0:
                        print("FOURTH IF STATEMENT:::::")
                        self.amountpaid = decimal.Decimal(self.amountpaid) + f.amountpaid
                        # paid = decimal.Decimal(self.amountpaid)
                        self.balance = f.balance - amountEntered
                        self.total = actualfees

                    if f.semester == self.semester and f.balance < 0:
                        print("FIFTH IF STATEMENT:::::")
                        self.amountpaid = decimal.Decimal(self.amountpaid) + f.amountpaid
                        # paid = decimal.Decimal(self.amountpaid)
                        self.balance = f.balance - amountEntered
                        self.total = actualfees


            else:
                self.balance = actualfees - decimal.Decimal(self.amountpaid)
                self.total = actualfees

            if self.balance > 0:
                self.paystatus = 'Got Balance'

            # activate the user upon subscription
            # u = User.objects.get(pk=self.user.pk)
            # u.is_active = True
            # u.save(force_update=u.is_active)

            super(SchoolFees, self).save()

    def __str__(self):
        return str(self.student) + ' - ' + str(self.gradefees)


class SchoolDetails(models.Model):
    schoolname = models.CharField('Name Of School', max_length=500, default='')
    address = models.CharField('School Address', max_length=200, null=True, blank=True, default='School Address')
    email = models.CharField('Email Address', max_length=200, null=True, blank=True,
                             default='exampleemail@exampleemail.com')
    phone = models.CharField('Tel/Cell', max_length=200, null=True, blank=True, default='Tel/Cell Number')
    photo = models.ImageField('School logo', upload_to='school/logo/%Y/%m/%d', default='', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'School Details'
        verbose_name = 'School Details'

    def __str__(self):
        return self.schoolname


class PupilAttendance(models.Model):
    nameofclass = models.ForeignKey(SchoolClass, verbose_name='Class', default='', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name='Student', default='', on_delete=models.CASCADE)
    #course = models.ForeignKey(Course, verbose_name='Course', default='', on_delete=models.CASCADE)
    mark_attendance = models.CharField(max_length=50, default='Present', choices=class_attendance)
    daysdate = models.DateField('Attended On', default='')

    class Meta:
        verbose_name = 'Student Attendance'
        verbose_name_plural = 'Student Attendance'

    def __str__(self):
        return str(self.nameofclass) + ' - ' + str(self.student)


class AllDepartmentsList(models.Model):
    departmentname = models.CharField('Name Of Department', max_length=200, default='')

    class Meta:
        verbose_name = 'All School Departments'
        verbose_name_plural = 'All School Departments'

    def __str__(self):
        return self.departmentname


class DepartmentOfTeacher(models.Model):
    department = models.ForeignKey(AllDepartmentsList, verbose_name='Name Of Department', default='',
                                   on_delete=models.CASCADE)
    teacher = models.CharField('Teacher', default='', max_length=200)

    class Meta:
        verbose_name = 'Teacher And Department'
        verbose_name_plural = 'Teacher And Department'

    def __str__(self):
        return str(self.department) + ' - ' + str(self.teacher)


class Announcement(models.Model):
    teacher = models.ForeignKey(User, max_length=200, verbose_name='Teachers Name', on_delete=models.CASCADE)
    announcement = models.TextField('News Details', max_length=10000, )
    announcementdatetime = models.DateTimeField(auto_now=True, verbose_name='Date')

    class Meta:
        verbose_name_plural = 'Announcements'
        verbose_name = 'Announcement'

    def __str__(self):
        return str(self.teacher) + ' - ' + self.announcement

DAYS = (
    ("Sun", "Sunday"),
    ("Mon", "Monday"),
    ("Tue", "Tuesday"),
    ("Wed", "Wednesday"),
    ("Thur", "Thursday"),
    ("Fri", "Friday"),
    ("Sat", "Saturday"),
)

class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField('Day', choices=DAYS, max_length=20)
    start_time = models.TimeField('Start Time', )
    end_time = models.TimeField('End Time', )
    venue = models.CharField('Venue', max_length=200, null=True, blank=True, help_text='Optional')
    description = models.CharField('Description', max_length=200, null=True, blank=True, help_text='Optional')

    def __str__(self):
        return str(self.course.courseTitle)