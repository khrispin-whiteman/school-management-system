from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import datetime
# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from library.models import Book
from school.decorators import lecturer_required, student_required
from school.forms import StudentCourseRegistrationForm, CourseAllocationForm, CourseAddForm, StudentAddForm, \
    StaffAddForm, SemesterForm, SessionForm, SchoolClassAddForm, FeesCollectionForm, ProfileForm, SchoolClassEditForm, \
    StudentAttendanceForm, ParentAddForm, ParentChildrenAddForm, SchoolDetails, FeesStructureAddForm
from school.models import CourseAllocation, Result, Student, TakenCourse, Semester, Course, Session, SchoolClass, User, \
    SchoolFees, Level, Parent, Timetable, PupilAttendance, Fees


def index(request):
    schooldetails = SchoolDetails.objects.all()
    return render(request, 'frontend/index.html',
                  {
                      'schooldetails': schooldetails,
                  })


def schoolpackages(request):
    return render(request, 'frontend/packages.html', {})


@login_required
def home(request):
    """
    Shows our dashboard containing number of students, courses, lecturers, repating students,
    carry over students and 1st class students in an interactive graph

    """
    students = Student.objects.all().count()
    parents = Parent.objects.all().count()
    staff = User.objects.filter(is_lecturer=True).count()
    courses = Course.objects.all().count()
    current_semester = Semester.objects.get(is_current_semester=True)
    no_of_1st_class_students = Result.objects.filter(cgpa__gte=4.5).count()
    # no_of_carry_over_students = CarryOverStudent.objects.all().count()
    # no_of_students_to_repeat = RepeatingStudent.objects.all().count()

    context = {
        "no_of_students": students,
        "no_of_parents": parents,
        "no_of_staff": staff,
        "no_of_courses": courses,
        "no_of_1st_class_students": no_of_1st_class_students,
        # "no_of_students_to_repeat": no_of_students_to_repeat,
        # "no_of_carry_over_students": no_of_carry_over_students,
    }

    return render(request, 'school/home.html', context)


def get_chart(request, *args, **kwargs):
    all_query_score = ()
    levels = (1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13)  # all the levels in the department

    # levels = Level.objects.all()

    # iterate through the levels above
    for i in levels:
        # gather all the courses registered by the students of the current level in the loop
        # all_query_score += (TakenCourse.objects.filter(student__level=i.level, semester__is_current_semester=True),)
        all_query_score += (TakenCourse.objects.filter(student__level=i),)
        # print(all_query_score)

    # for level #100
    first_level_total = 0

    # get the total score for all the courses registered by the students of this level
    for i in all_query_score[0]:
        first_level_total += i.total
    first_level_avg = 0
    if not all_query_score[0].count() == 0:
        # calculate the average of all the students of this level
        first_level_avg = first_level_total / all_query_score[0].count()

    # do same  as above for # 200 Level students
    second_level_total = 0
    for i in all_query_score[1]:
        second_level_total += i.total
    second_level_avg = 0
    if not all_query_score[1].count() == 0:
        second_level_avg = second_level_total / all_query_score[1].count()

    # do same  as above for # 300 Level students
    third_level_total = 0
    for i in all_query_score[2]:
        third_level_total += i.total
    third_level_avg = 0
    if not all_query_score[2].count() == 0:
        third_level_avg = third_level_total / all_query_score[2].count()

    # do same  as above for # 400 Level students
    fourth_level_total = 0
    for i in all_query_score[3]:
        fourth_level_total += i.total
    fourth_level_avg = 0
    if not all_query_score[3].count() == 0:
        fourth_level_avg = fourth_level_total / all_query_score[3].count()

    # do same  as above for # 5 Level students
    fifth_level_total = 0
    for i in all_query_score[4]:
        fifth_level_total += i.total
    fifth_level_avg = 0
    if not all_query_score[4].count() == 0:
        fifth_level_avg = fifth_level_total / all_query_score[4].count()

    # GRADE 6
    sixth_level_total = 0
    for i in all_query_score[5]:
        sixth_level_total += i.total
    sixth_level_avg = 0
    if not all_query_score[5].count() == 0:
        sixth_level_avg = sixth_level_total / all_query_score[5].count()

    # Grade 7
    seventh_level_total = 0
    for i in all_query_score[6]:
        seventh_level_total += i.total
    seventh_level_avg = 0
    if not all_query_score[6].count() == 0:
        seventh_level_avg = seventh_level_total / all_query_score[6].count()

    # Grade 8
    eighth_level_total = 0
    for i in all_query_score[7]:
        eighth_level_total += i.total
    eighth_level_avg = 0
    if not all_query_score[7].count() == 0:
        eighth_level_avg = eighth_level_total / all_query_score[7].count()

    # Grade 9
    ninth_level_total = 0
    for i in all_query_score[8]:
        ninth_level_total += i.total
    ninth_level_avg = 0
    if not all_query_score[8].count() == 0:
        ninth_level_avg = ninth_level_total / all_query_score[8].count()

    # Grade 10
    tenth_level_total = 0
    for i in all_query_score[9]:
        tenth_level_total += i.total
    tenth_level_avg = 0
    if not all_query_score[9].count() == 0:
        tenth_level_avg = tenth_level_total / all_query_score[9].count()

    # Grade 11
    eleventh_level_total = 0
    for i in all_query_score[10]:
        eleventh_level_total += i.total
    eleventh_level_avg = 0
    if not all_query_score[10].count() == 0:
        eleventh_level_avg = eleventh_level_total / all_query_score[10].count()

    # Grade 12
    twelveth_level_total = 0
    for i in all_query_score[11]:
        twelveth_level_total += i.total
    twelveth_level_avg = 0
    if not all_query_score[11].count() == 0:
        twelveth_level_avg = twelveth_level_total / all_query_score[11].count()

    # do same  as above for # 6 Level students
    # sixth_level_total = 0
    # for i in all_query_score[5]:
    #     sixth_level_total += i.total
    # sixth_level_avg = 0
    # if not all_query_score[5].count() == 0:
    #     sixth_level_avg = sixth_level_total / all_query_score[5].count()

    labels = ["G-1", "G-2", "G-3", "G-4", "G-5", "G-6", "G-7", "G-8", "G-9", "G-10", "G-11", "G-12"]
    default_level_average = [first_level_avg, second_level_avg, third_level_avg, fourth_level_avg, fifth_level_avg,
                             sixth_level_avg, seventh_level_avg, eighth_level_avg, ninth_level_avg, tenth_level_avg,
                             eleventh_level_avg, twelveth_level_avg
                             ]
    average_data = {
        "labels": labels,
        "default_level_average": default_level_average,
    }
    return JsonResponse(average_data)


@login_required
def profile(request):
    """ Show profile of any user that fire out the request """
    current_semester = Semester.objects.get(is_current_semester=True)
    if request.user.is_lecturer:
        print("IF LECTUREr::")
        courses = Course.objects.filter(allocated_course__lecturer__pk=request.user.id).filter(
            semester=current_semester)
        return render(request, 'account/profile.html', {"courses": courses, })
    elif request.user.is_student:
        print("IF STUDENT::")
        level = Student.objects.get(user__pk=request.user.id)
        courses = TakenCourse.objects.filter(student__user__id=request.user.id, course__level=level.level)

        context = {
            'courses': courses,
            'level': level,
        }
        return render(request, 'account/profile.html', context)
    elif request.user.is_parent:
        print("IF parent::")
        parent = Parent.objects.get(user__pk=request.user.id)
        # student = Student.objects.get(user__pk=parent.student.id)
        # courses = TakenCourse.objects.filter(student__user__id=parent.student.id, )

        context = {
            # 'courses': courses,
            # 'level': level,
            'parent': parent,
        }
        return render(request, 'account/profile.html', context)
    elif request.user.is_librarian:
        print("IF LIBRARIAN::")
        books = Book.objects.all()
        return render(request, 'account/profile.html',
                      {
                          "books": books,
                      })
    else:
        staff = User.objects.filter(is_lecturer=True)
        return render(request, 'account/profile.html', {"staff": staff})


@login_required
def user_profile(request, id):
    """ Show profile of any selected user """
    if request.user.id == id:
        return redirect("/profile/")

    current_semester = Semester.objects.get(is_current_semester=True)
    user = User.objects.get(pk=id)
    if user.is_lecturer:
        courses = Course.objects.filter(allocated_course__lecturer__pk=id).filter(semester=current_semester)
        context = {
            "user": user,
            "courses": courses,
        }
        return render(request, 'account/user_profile.html', context)
    elif user.is_student:
        level = Student.objects.get(user__pk=id)
        courses = TakenCourse.objects.filter(student__user__id=id, course__level=level.level,
                                             semester__is_current_semester=True)
        context = {
            "user_type": "student",
            'courses': courses,
            'level': level,
            'user': user,
        }
        return render(request, 'account/user_profile.html', context)

    elif user.is_librarian:
        books = Book.objects.all()
        return render(request, 'account/user_profile.html',
                      {
                          "books": books,
                      })
    else:
        context = {
            "user": user,
            "user_type": "superuser"
        }
        return render(request, 'account/user_profile.html', context)


@login_required
def pay_history(request):
    if request.user.is_parent:
        parent = User.objects.get(id=request.user.id)
        students = parent.student.all()

        # schoolfees = []
        # for s in students:
        #     schoolfees.extend(SchoolFees.objects.filter(student__user__id=s.id))

        return render(request, 'students/pay_history.html',
                      {
                          'students': students,
                      })

    elif request.user.is_student:
        schoolfees = SchoolFees.objects.filter(student__user__id=request.user.id)
        return render(request, 'students/pay_history.html',
                      {
                          'schoolfees': schoolfees,
                      })


@login_required
def parent_payment_history_view(request, pk):
    schoolfees = SchoolFees.objects.filter(student__id=pk)
    return render(request, 'parent/parent_payment_history_view.html',
                  {
                      'schoolfees': schoolfees,
                  })


# def pay_history_report()
@login_required
def profile_update(request):
    """ Check if the fired request is a POST then grab changes and update the records otherwise we show an empty form """
    user = request.user.id
    user = User.objects.get(pk=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.phone = form.cleaned_data.get('phone')
            user.address = form.cleaned_data.get('address')
            if request.FILES:
                user.picture = request.FILES['picture']
            user.save()
            messages.success(request, 'Your profile was successfully edited.')
            return redirect("/profile/")
    else:
        form = ProfileForm(instance=user, initial={
            'firstname': user.first_name,
            'lastname': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'picture': user.picture,
        })

    return render(request, 'account/profile_update.html', {'form': form})


@login_required
@lecturer_required
def course_list(request):
    """ Show list of all registered courses in the system """
    courses = Course.objects.all()
    context = {
        "courses": courses,
    }
    return render(request, 'administrator/course_list.html', context)


@login_required
@lecturer_required
def student_list(request):
    """ Show list of all registered students in the system """
    students = Student.objects.all()
    class_count = SchoolClass.objects.all().count()
    user_type = "Student"
    context = {
        "students": students,
        "user_type": user_type,
        'class_count': class_count,
    }
    return render(request, 'students/student_list.html', context)


@login_required
def student_fees(request):
    """ Show list of all registered students in the system """
    students = Student.objects.all()
    fees = SchoolFees.objects.all()
    user_type = "Fees"
    context = {
        "students": students,
        "fees": fees,
        "user_type": user_type,
    }
    return render(request, 'administrator/manage_fees_collection.html', context)


@login_required
def fees_structure(request):
    """ Show list of all registered students in the system """
    fees_strcture = Fees.objects.all()
    user_type = "Fees"
    context = {
        "fees": fees_strcture,
        "user_type": user_type,
    }
    return render(request, 'administrator/fees_structures_list.html', context)


@method_decorator([login_required, ], name='dispatch')
class FeesCollectionView(CreateView):
    model = SchoolFees
    form_class = FeesCollectionForm
    template_name = 'administrator/fees_collection_form.html'

    def form_valid(self, form):
        form.save()
        return redirect('student_fees')


@method_decorator([login_required, ], name='dispatch')
class FeesStructureAddView(CreateView):
    model = Fees
    form_class = FeesStructureAddForm
    template_name = 'administrator/fees_add_form.html'

    def form_valid(self, form):
        form.save()
        return redirect('fees_structure_list')


@login_required
def edit_fee_structure(request, pk):
    f_structure = get_object_or_404(Fees, pk=pk)
    if request.method == "POST":
        form = FeesStructureAddForm(request.POST, instance=f_structure)
        if form.is_valid():
            f_structure.save()
            return redirect('fees_structure_list')
    else:
        form = FeesStructureAddForm(instance=f_structure)
    return render(request, 'administrator/edit_fee_structure.html', {'form': form})


@login_required
def fee_structure_delete_view(request, pk):
    f_structure = get_object_or_404(Fees, pk=pk)
    f_structure.delete()
    messages.success(request, "Session successfully deleted")
    return redirect('fees_structure_list')


@login_required
@lecturer_required
def manage_classes(request):
    """ Show list of all registered classes in the system """
    classes = SchoolClass.objects.all()
    # fees = SchoolFees.objects.all()
    user_type = "Classes"
    context = {
        "classes": classes,
        # "fees": fees,
        "user_type": user_type,
    }
    return render(request, 'administrator/manage_classes.html', context)


@login_required
@lecturer_required
def view_class(request, pk):
    thisclass = SchoolClass.objects.get(id=pk)
    level = Level.objects.get(id=pk)
    students = Student.objects.filter(level=thisclass.grade)
    print('CLASS TEACHER:: ', thisclass.classteacher)
    # fees = SchoolFees.objects.all()
    user_type = str(thisclass.grade) + ' - ' + thisclass.classname
    context = {
        "thisclass": thisclass,
        "students": students,
        "user_type": user_type,
    }
    return render(request, 'administrator/class_detail_view.html', context)


def get_courses_for_class(request, pk):
    thisclass = SchoolClass.objects.get(id=pk)
    user_type = str(thisclass.grade) + ' - ' + thisclass.classname
    context = {
        "thisclass": thisclass,
        "user_type": user_type,
    }
    return render(request, 'administrator/courses_for_class.html', context)


@method_decorator([login_required, ], name='dispatch')
class SchoolClassAddView(CreateView):
    model = SchoolClass
    form_class = SchoolClassAddForm
    # teachers = User.objects.get(is_lecturer=False)
    template_name = 'administrator/add_class.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'class'
        kwargs['teachers'] = User.objects.filter(is_lecturer=True)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('manage_classes')


@login_required
@lecturer_required
def student_attendance_list_by_class(request):
    """ Show list of all registered students in the system """
    if request.user.is_lecturer is True:
        students = Student.objects.all()
        fees = SchoolFees.objects.all()
        user_type = "Attendance By Class"
        school_class = SchoolClass.objects.filter(classteacher__id=request.user.id)
        context = {
            "students": students,
            "fees": fees,
            "user_type": user_type,
            "school_class": school_class,
        }
        return render(request, 'students/attendance_list_by_class.html', context)
    if request.user.is_superuser is True:
        students = Student.objects.all()
        fees = SchoolFees.objects.all()
        user_type = "Attendance By Class"
        school_class = SchoolClass.objects.all()
        context = {
            "students": students,
            "fees": fees,
            "user_type": user_type,
            "school_class": school_class,
        }
        return render(request, 'students/attendance_list_by_class.html', context)


@login_required
@lecturer_required
def student_attendance_mark(request, pk):
    """ Show list of all registered students in the system """
    school_class = SchoolClass.objects.get(pk=pk, )
    students = Student.objects.filter(schoolclass=school_class)
    # fees = SchoolFees.objects.all()
    count = students.count()
    attendance_formset = formset_factory(StudentAttendanceForm, extra=count)
    date = datetime.today().date().strftime('%d-%m-%Y')

    if request.method == 'POST':
        formset = attendance_formset(request.POST)
        list = zip(students, formset)

        if formset.is_valid():
            for form, student in zip(formset, students):
                date = datetime.today()
                mark = form.cleaned_data['mark_attendance']
                print(mark)
                check_attendance = PupilAttendance.objects.filter(nameofclass=school_class, daysdate=date,
                                                                  student=student)
                print(check_attendance)

                # if check_attendance:
                #     attendance = PupilAttendance.objects.get(nameofclass=schoolClass, daysdate=date, student=student)
                #     if attendance.mark_attendance == 'Absent':
                #         student.absent = student.absent - 1
                #     elif attendance.mark_attendance == 'Present':
                #         student.present = student.present - 1
                #     attendance.mark_attendance = mark
                #     attendance.save()

                if check_attendance:
                    attendance = PupilAttendance.objects.get(nameofclass=school_class, daysdate=date, student=student)
                    if attendance.mark_attendance == 'Absent':
                        if mark == 'Absent':
                            attendance.mark_attendance = mark
                        if mark == 'Present':
                            attendance.mark_attendance = mark
                    elif attendance.mark_attendance == 'Present':
                        if mark == 'Absent':
                            attendance.mark_attendance = mark
                        if mark == 'Present':
                            attendance.mark_attendance = mark
                    # attendance.mark_attendance = mark
                    attendance.save()

                else:
                    attendance = PupilAttendance()
                    attendance.nameofclass = school_class
                    attendance.student = student
                    attendance.daysdate = date
                    if mark == 'Absent':
                        attendance.mark_attendance = mark
                    if mark == 'Present':
                        attendance.mark_attendance = mark
                    attendance.save()

                # if mark == 'Absent':
                #     student.absent = student.absent + 1
                # if mark == 'Present':
                #     student.present = student.present + 1
                # student.save()

            context = {
                'students': students,
                'school_class': school_class,
            }
            # return render(request, 'attendance/profile.html', context)
            return redirect('student_attendance_mark', school_class.pk)
        else:
            error = "Something went wrong"
            context = {
                'error': error,
                'formset': formset,
                'students': students,
                'school_class': school_class,
                'list': list,
                'date': date,
            }
            return render(request, 'students/attendance_mark.html', context)

    else:
        list = zip(students, attendance_formset())
        context = {
            'formset': attendance_formset(),
            'students': students,
            'school_class': school_class,
            'list': list,
            'date': date,
        }

        return render(request, 'students/attendance_mark.html', context)

    # user_type = schoolClass
    # # school_class = SchoolClass.objects.all()
    # context = {
    #     "students": students,
    #     "fees": fees,
    #     "user_type": user_type,
    #     "school_class": schoolClass,
    # }
    # return render(request, 'students/attendance_mark.html', context)


@login_required
def student_attendance_archive(request, class_id):
    pupil_attendance = PupilAttendance.objects.filter(nameofclass__id=class_id)
    school_class = SchoolClass.objects.get(id=class_id)
    return render(request, 'students/student_attendance_archive.html',
                  {
                      'pupil_attendance': pupil_attendance,
                      'school_class': school_class,
                  })


@login_required
@lecturer_required
def staff_list(request):
    """ Show list of all registered staff """
    staff = User.objects.filter(is_student=False, is_parent=False)
    user_type = "Staff"
    context = {
        "staff": staff,
        "user_type": user_type,
    }
    return render(request, 'staff/staff_list.html', context)


@login_required
def parent_list(request):
    """ Show list of all registered staff """
    parent = User.objects.filter(is_parent=True)
    user_type = "Parent"
    context = {
        "parents": parent,
        "user_type": user_type,
    }
    return render(request, 'parent/parent_list.html', context)


@login_required
def session_list_view(request):
    """ Show list of all sessions """
    sessions = Session.objects.all().order_by('-session')
    return render(request, 'administrator/manage_session.html', {"sessions": sessions, })


@login_required
@lecturer_required
def session_add_view(request):
    """ check request method, if POST we add session otherwise show empty form """
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Session added successfully ! ')

    else:
        form = SessionForm()
    return render(request, 'administrator/session_update.html', {'form': form})


@login_required
@lecturer_required
def session_update_view(request, pk):
    session = Session.objects.get(pk=pk)
    if request.method == 'POST':
        a = request.POST.get('is_current_session')
        if a == '2':
            unset = Session.objects.get(is_current_session=True)
            unset.is_current_session = False
            unset.save()
            form = SessionForm(request.POST, instance=session)
            if form.is_valid():
                form.save()
                messages.success(request, 'Session updated successfully ! ')
        else:
            form = SessionForm(request.POST, instance=session)
            if form.is_valid():
                form.save()
                messages.success(request, 'Session updated successfully ! ')

    else:
        form = SessionForm(instance=session)
    return render(request, 'administrator/session_update.html', {'form': form})


@login_required
def session_delete_view(request, pk):
    session = get_object_or_404(Session, pk=pk)
    if session.is_current_session == True:
        messages.info(request, "You cannot delete current session")
        return redirect('manage_session')
    else:
        session.delete()
        messages.success(request, "Session successfully deleted")
    return redirect('manage_semester')


@login_required
def semester_list_view(request):
    semesters = Semester.objects.all().order_by('-semester')
    return render(request, 'administrator/manage_semester.html', {"semesters": semesters, })


@login_required
def semester_add_view(request):
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            data = form.data.get('is_current_semester')  # returns string of 'True' if the user selected Yes
            if data == 'True':
                semester = form.data.get('semester')
                ss = form.data.get('session')
                session = Session.objects.get(pk=ss)
                try:
                    if Semester.objects.get(semester=semester, session=ss):
                        messages.info(request, semester + " semester in " + session.session + " session already exist")
                        return redirect('create_new_semester')
                except:
                    semester = Semester.objects.get(is_current_semester=True)
                    semester.is_current_semester = False
                    semester.save()
                    form.save()
            form.save()
            messages.success(request, 'Semester added successfully ! ')
            return redirect('manage_semester')
    else:
        form = SemesterForm()
    return render(request, 'administrator/semester_update.html', {'form': form})


@login_required
def semester_update_view(request, pk):
    semester = Semester.objects.get(pk=pk)
    if request.method == 'POST':
        if request.POST.get(
                'is_current_semester') == 'True':  # returns string of 'True' if the user selected yes for 'is current semester'
            unset_semester = Semester.objects.get(is_current_semester=True)
            unset_semester.is_current_semester = False
            unset_semester.save()
            unset_session = Session.objects.get(is_current_session=True)
            unset_session.is_current_session = False
            unset_session.save()
            new_session = request.POST.get('session')
            form = SemesterForm(request.POST, instance=semester)
            if form.is_valid():
                set_session = Session.objects.get(pk=new_session)
                set_session.is_current_session = True
                set_session.save()
                form.save()
                messages.success(request, 'Semester updated successfully !')
                return redirect('manage_semester')
        else:
            form = SemesterForm(request.POST, instance=semester)
            if form.is_valid():
                form.save()
                return redirect('manage_semester')

    else:
        form = SemesterForm(instance=semester)
    return render(request, 'administrator/semester_update.html', {'form': form})


@login_required
def semester_delete_view(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if semester.is_current_semester == True:
        messages.info(request, "You cannot delete current semester")
        return redirect('manage_semester')
    else:
        semester.delete()
        messages.success(request, "Semester successfully deleted")
    return redirect('manage_semester')


@method_decorator([login_required, lecturer_required], name='dispatch')
class StaffAddView(CreateView):
    model = User
    form_class = StaffAddForm
    template_name = 'administrator/add_staff.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'staff'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('staff_list')


@method_decorator([login_required, lecturer_required], name='dispatch')
class ParentAddView(CreateView):
    model = User
    form_class = ParentAddForm
    template_name = 'parent/add_parent.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'parent'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('add_new_parents_child', pk=user.id)


@method_decorator([login_required, lecturer_required], name='dispatch')
class ParentChildrenAddView(CreateView):
    model = User
    form_class = ParentChildrenAddForm
    template_name = 'parent/add_parents_children.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'parent'
        kwargs['pk'] = self.kwargs['pk']
        kwargs['parent'] = User.objects.get(id=self.kwargs['pk'])
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('parent_list')


@login_required
def parent_details(request, pk):
    parent = User.objects.get(is_parent=True, id=pk)

    students = Student.objects.filter(parent__user_id=pk)
    return render(request, 'parent/parent_detail.html',
                  {

                      'parent': parent,
                      'students': students,

                  })

    # try:
    #     students = parent.student()
    #     return render(request, 'parent/parent_detail.html',
    #                   {
    #
    #                       'parent': parent,
    #                       'students': students,
    #
    #                   })
    # except User.student.RelatedObjectDoesNotExist:
    #     return render(request, 'parent/parent_detail.html',
    #                   {
    #
    #                       'parent': parent,
    #                       # 'students': students,
    #
    #                   })

    # takencourse = TakenCourse.objects.filter(student__id=pk, semester__is_current_semester=True)


@login_required
def edit_staff(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.phone = form.cleaned_data.get('phone')
            user.address = form.cleaned_data.get('address')
            if request.FILES:
                user.picture = request.FILES['picture']
            user.save()
            messages.success(request, 'Your profile was successfully edited.')
            return redirect("user_profile", pk)
    else:
        form = ProfileForm(instance=user, initial={
            'firstname': user.first_name,
            'lastname': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'picture': user.picture,
        })

    return render(request, 'account/edit_staff_admin.html',
                  {
                      'form': form,
                      'staff_id': pk,
                  })


@login_required
def edit_parent(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.phone = form.cleaned_data.get('phone')
            user.address = form.cleaned_data.get('address')
            if request.FILES:
                user.picture = request.FILES['picture']
            user.save()
            messages.success(request, 'Your profile was successfully edited.')
            return redirect("parent_details", pk)
    else:
        form = ProfileForm(instance=user, initial={
            'firstname': user.first_name,
            'lastname': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'picture': user.picture,
        })

    return render(request, 'account/edit_parent_admin.html',
                  {
                      'form': form,
                      'parent_id': pk,
                  })


@login_required
@lecturer_required
def delete_staff(request, pk):
    staff = get_object_or_404(User, pk=pk)
    staff.delete()
    return redirect('staff_list')


@login_required
@lecturer_required
def make_staff_admin(request, pk):
    staff = get_object_or_404(User, pk=pk)
    staff.is_superuser = True
    staff.save()
    return redirect('staff_list')


@login_required
def remove_staff_admin(request, pk):
    staff = get_object_or_404(User, pk=pk)
    staff.is_superuser = False
    staff.save()
    return redirect('staff_list')


@method_decorator([login_required, lecturer_required], name='dispatch')
class StudentAddView(CreateView):
    model = User
    form_class = StudentAddForm
    template_name = 'administrator/add_student.html'
    classlist = SchoolClass.objects.all()

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        kwargs['classlist'] = course_list
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('student_list')


@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    user = User.objects.get(pk=student.user.pk)

    print("STUDENT NAME: ", user.first_name)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            student.user.first_name = form.cleaned_data.get('first_name')
            student.user.last_name = form.cleaned_data.get('last_name')
            student.user.email = form.cleaned_data.get('email')
            student.user.phone = form.cleaned_data.get('phone')
            student.user.address = form.cleaned_data.get('address')
            if request.FILES:
                student.user.picture = request.FILES['picture']
            student.user.save()
            messages.success(request, 'Profile was successfully edited.')
            return redirect("student_details", pk)
    else:
        form = ProfileForm(instance=user, initial={
            'firstname': student.user.first_name,
            'lastname': student.user.last_name,
            'email': student.user.email,
            'phone': student.user.phone,
            'picture': student.user.picture,
        })

    return render(request, 'administrator/edit_student_admin.html',
                  {
                      'form': form,
                      'student_id': pk,
                  })


@login_required
@lecturer_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('student_list')


@method_decorator([login_required, lecturer_required], name='dispatch')
class CourseAddView(CreateView):
    model = Course
    form_class = CourseAddForm
    template_name = 'administrator/course_form.html'

    def form_valid(self, form):
        form.save()
        return redirect('course_allocation')


@login_required
@lecturer_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = CourseAddForm(request.POST, instance=course)
        if form.is_valid():
            course.save()
            messages.success(request, "Successfully Updated")
            return redirect('course_list')
    else:
        form = CourseAddForm(instance=course)
    return render(request, 'administrator/course_form.html', {'form': form})


@login_required
@lecturer_required
def class_edit(request, pk):
    thisclass = get_object_or_404(SchoolClass, pk=pk)
    if request.method == 'POST':
        form = SchoolClassEditForm(request.POST)
        if form.is_valid():
            thisclass.grade = form.cleaned_data.get('grade')
            thisclass.classname = form.cleaned_data.get('classname')
            thisclass.classteacher = form.cleaned_data.get('classteacher')
            # thisclass.grade = form.cleaned_data.get('grade')
            # user.last_name = form.cleaned_data.get('last_name')
            # user.email = form.cleaned_data.get('email')
            # user.phone = form.cleaned_data.get('phone')
            # user.address = form.cleaned_data.get('address')
            # if request.FILES:
            #     user.picture = request.FILES['picture']
            # user.save()
            thisclass.save()
            messages.success(request, 'Class was successfully edited.')
            return redirect("manage_classes")
    else:
        form = SchoolClassEditForm(instance=thisclass, initial={
            'classname': thisclass.classname,
            'classteacher': thisclass.classteacher,
            'grade': thisclass.grade,
            'courses': thisclass.courses.all(),
        })

    return render(request, 'administrator/edit_class_form.html', {'form': form})

    # thisclass = get_object_or_404(SchoolClass, pk=pk)
    # if request.method == "POST":
    #     form = SchoolClassEditForm(request.POST, instance=thisclass)
    #     if form.is_valid():
    #         thisclass.save()
    #         messages.success(request, "Successfully Updated")
    #         return redirect('manage_classes')
    # else:
    #     form = SchoolClassEditForm(instance=thisclass)
    # return render(request, 'administrator/edit_class_form.html',
    #               {
    #                   'form': form,
    #                   'thisclass': thisclass,
    #               })


@method_decorator([login_required, lecturer_required], name='dispatch')
class CourseAllocationView(CreateView):
    form_class = CourseAllocationForm
    template_name = 'administrator/course_allocation.html'

    def get_form_kwargs(self):
        kwargs = super(CourseAllocationView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # if a staff has been allocated a course before update it else create new
        lecturer = form.cleaned_data['lecturer']
        selected_courses = form.cleaned_data['courses']
        courses = ()
        for course in selected_courses:
            courses += (course.pk,)
        print(courses)

        try:
            a = CourseAllocation.objects.get(lecturer=lecturer)
        except:
            a = CourseAllocation.objects.create(lecturer=lecturer)
        for i in range(0, selected_courses.count()):
            a.courses.add(courses[i])
            a.save()
        return redirect('course_allocation_view')


@method_decorator([login_required, student_required], name='dispatch')
class StudentCourseRegistation(CreateView):
    model = TakenCourse
    form_class = StudentCourseRegistrationForm
    template_name = 'administrator/student_course_registration.html'

    def form_valid(self, form):
        form.save()
        return redirect('student_list')


@login_required
def view_student_details(request, pk):
    student = Student.objects.get(id=pk)
    takencourse = TakenCourse.objects.filter(student__id=pk, semester__is_current_semester=True)

    return render(request, 'students/view_student_details.html',
                  {

                      'student': student,
                      'takencourse': takencourse,

                  })


@login_required
@student_required
def course_drop(request):
    if request.method == 'POST':
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)  # remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)
        for s in range(0, len(ids)):
            student = Student.objects.get(user__pk=request.user.id)
            course = Course.objects.get(pk=ids[s])
            obj = TakenCourse.objects.get(student=student, course=course)
            obj.delete()
            messages.success(request, 'Successfully Dropped!')
        return redirect('course_registration')


@login_required
@lecturer_required
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    messages.success(request, 'Deleted successfully!')
    return redirect('course_list')


@login_required
@lecturer_required
def add_score(request):
    """
    Shows a page where a lecturer will select a course allocated to him for score entry.
    in a specific semester and session

    """
    current_session = Session.objects.get(is_current_session=True)
    current_semester = get_object_or_404(Semester, is_current_semester=True, session=current_session)
    semester = Course.objects.filter(allocated_course__lecturer__pk=request.user.id, semester=current_semester)
    courses = Course.objects.filter(allocated_course__lecturer__pk=request.user.id).filter(semester=current_semester)
    context = {
        "courses": courses,
    }
    return render(request, 'administrator/add_score.html', context)


@login_required
@lecturer_required
def add_score_for(request, id):
    """
    Shows a page where a lecturer will add score for studens that are taking courses allocated to him
    in a specific semester and session
    """
    current_semester = Semester.objects.get(is_current_semester=True)
    if request.method == 'GET':
        courses = Course.objects.filter(allocated_course__lecturer__pk=request.user.id).filter(
            semester=current_semester)
        course = Course.objects.get(pk=id)
        students = TakenCourse.objects.filter(course__allocated_course__lecturer__pk=request.user.id).filter(
            course__id=id).filter(course__semester=current_semester)
        context = {
            "courses": courses,
            "course": course,
            "students": students,
        }
        return render(request, 'administrator/add_score_for.html', context)

    if request.method == 'POST':
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)  # remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)  # gather all the all students id (i.e the keys) in a tuple
        for s in range(0, len(ids)):  # iterate over the list of student ids gathered above
            student = TakenCourse.objects.get(id=ids[s])
            courses = Course.objects.filter(level=student.student.level).filter(
                semester=current_semester)  # all courses of a specific level in current semester
            total_unit_in_semester = 0
            for i in courses:
                if i == courses.count():
                    break
                else:
                    total_unit_in_semester += int(i.courseUnit)
            score = data.getlist(ids[s])  # get list of score for current student in the loop
            ca = score[0]  # subscript the list to get the fisrt value > ca score
            exam = score[1]  # do thesame for exam score
            obj = TakenCourse.objects.get(pk=ids[s])  # get the current student data
            obj.ca = ca  # set current student ca score
            obj.exam = exam  # set current student exam score
            obj.total = obj.get_total(ca=ca, exam=exam)
            obj.grade = obj.get_grade(ca=ca, exam=exam)
            obj.comment = obj.get_comment(obj.grade)
            obj.carry_over(obj.grade)
            obj.is_repeating()
            obj.save()
            # gpa = obj.calculate_gpa(total_unit_in_semester)
            # cgpa = obj.calculate_cgpa()
            # try:
            #     a = Result.objects.get(student=student.student, semester=current_semester, level=student.student.level)
            #     a.gpa = gpa
            #     a.cgpa = cgpa
            #     a.save()
            # except:
            #     Result.objects.get_or_create(student=student.student, gpa=gpa, semester=current_semester, level=student.student.level)
        messages.success(request, 'Successfully Recorded! ')
        return HttpResponseRedirect(reverse_lazy('add_score_for', kwargs={'id': id}))
    return HttpResponseRedirect(reverse_lazy('add_score_for', kwargs={'id': id}))


@login_required
@student_required
def view_result(request):
    if request.user.is_parent:
        parent = Parent.objects.get(user=request.user)
        students = parent.student.all()

        context = {
            'students': students,
        }

        return render(request, 'students/view_results.html', context)

    elif request.user.is_student:
        student = Student.objects.get(user__pk=request.user.id)
        courses = TakenCourse.objects.filter(student__user__pk=request.user.id)
        result = Result.objects.filter(student__user__pk=request.user.id)

        context = {
            "courses": courses,
            "result": result,
            "student": student,
        }

        return render(request, 'students/view_results.html', context)


@login_required
def student_attendance(request):
    if request.user.is_parent:
        parent = Parent.objects.get(user=request.user)
        students = parent.student.all()

        context = {
            'students': students,
        }

        return render(request, 'students/student_attendance.html', context)

    elif request.user.is_student:
        studentattendance = PupilAttendance.objects.filter(student__user__id=request.user.id)

        context = {
            'studentattendance': studentattendance,
        }

        return render(request, 'students/student_attendance.html', context)


@login_required
def parent_attendance_view(request, pk):
    studentattendance = PupilAttendance.objects.filter(student__user__id=pk)
    student = Student.objects.get(user__id=pk)
    context = {
        'student': student,
        'studentattendance': studentattendance,
    }

    return render(request, 'parent/parent_attendance_view.html', context)


# @login_required
# def mark_attendance(request,pk):
#     teacher = get_object_or_404(Teacher, pk=pk)
#     students = Student.objects.filter(student_teacher=teacher)
#     count = students.count()
#     attendance_formset = formset_factory(AttendanceForm, extra=count)
#     date = datetime.today().date().strftime('%d-%m-%Y')
#
#     if request.method == 'POST':
#         formset = attendance_formset(request.POST)
#         list = zip(students, formset)
#
#         if formset.is_valid():
#             for form, student in zip(formset, students):
#                 date = datetime.today()
#                 mark = form.cleaned_data['mark_attendance']
#                 print(mark)
#                 check_attendance = Attendance.objects.filter(teacher=teacher, date=date, student=student)
#                 print(check_attendance)
#
#                 if check_attendance:
#                     attendance = Attendance.objects.get(teacher=teacher, date=date, student=student)
#                     if attendance.mark_attendance == 'Absent':
#                         student.absent = student.absent - 1
#                     elif attendance.mark_attendance == 'Present':
#                         student.present = student.present - 1
#                     attendance.mark_attendance = mark
#                     attendance.save()
#
#                 else:
#                     attendance = Attendance()
#                     attendance.teacher = teacher
#                     attendance.student = student
#                     attendance.date = date
#                     attendance.mark_attendance = mark
#                     attendance.save()
#
#                 if mark == 'Absent':
#                     student.absent = student.absent + 1
#                 if mark == 'Present':
#                     student.present = student.present + 1
#                 student.save()
#
#             context = {
#                 'students': students,
#                 'teacher': teacher,
#             }
#             # return render(request, 'attendance/profile.html', context)
#             return redirect('attendance:profile', pk=teacher.pk)
#         else:
#             error = "Something went wrong"
#             context = {
#                 'error': error,
#                 'formset': formset,
#                 'students': students,
#                 'teacher': teacher,
#                 'list': list,
#                 'date': date,
#             }
#             return render(request, 'attendance/attendance_form.html', context)
#
#     else:
#         list = zip(students, attendance_formset())
#         context = {
#             'formset': attendance_formset(),
#             'students': students,
#             'teacher': teacher,
#             'list': list,
#             'date': date,
#         }
#
#         return render(request, 'attendance/attendance_form.html', context)


@login_required
@student_required
def view_result_by_parent(request, pk):
    student = Student.objects.get(id=pk)
    courses = TakenCourse.objects.filter(student__id=pk)
    result = Result.objects.filter(student__pk=pk)

    context = {
        "courses": courses,
        "result": result,
        "student": student,
        # "previousCGPA": previousCGPA,
    }

    return render(request, 'parent/parent_view_results.html', context)

    # current_semester = Semester.objects.get(is_current_semester=True)

    # courses = TakenCourse.objects.filter(student__user__pk=request.user.id)
    # result = Result.objects.filter(student__user__pk=request.user.id)
    # current_semester_grades = {}

    # print('CALLING VIEW_RESULTS')
    # for course in courses:
    #     print('TITLE:::', course.course.courseTitle)
    #     print('CODE:::', course.course.courseCode)
    #     print('GRADE:::', course.grade)
    #
    # previousCGPA = 0
    # previousLEVEL = 0

    # for i in result:
    #     if not int(i.level) - 100 == 0: # TODO think n check the logic
    #         previousLEVEL = i.level
    #         try:
    #             a = Result.objects.get(student__user__pk=request.user.id, level=previousLEVEL, semester="Second")
    #             previousCGPA = a.cgpa
    #             break
    #         except:
    #             previousCGPA = 0
    #     else:
    #         break


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
        # return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below. ')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {
        'form': form,
    })


@login_required
@lecturer_required
def course_allocation_view(request):
    allocated_courses = CourseAllocation.objects.all()
    return render(request, 'administrator/course_allocation_view.html', {"allocated_courses": allocated_courses})


@login_required
@lecturer_required
def withheld_course(request, pk):
    course = CourseAllocation.objects.get(pk=pk)
    course.delete()
    messages.success(request, 'successfully deallocated!')
    return redirect("course_allocation_view")


@login_required
def first_class_list(request):
    students = Result.objects.filter(cgpa__gte=4.5)
    return render(request, 'students/first_class_students.html', {"students": students})


def timetable_all(request):
    timetables = Timetable.objects.all()
    return render(request, 'administrator/timetable_all.html',
                  {
                      'timetables': timetables,
                  })


def timetable_by_day(request):
    timetables = Timetable.objects.all()
    return render(request, 'administrator/timetable_by_day.html',
                  {
                      'timetables': timetables,
                  })
