from django.urls import path
from .import views

urlpatterns = [
	path('index/', views.index, name="index"),
	path('', views.home, name="home"),
	path('score/', views.add_score, name='add_score'),
	path('score/<int:id>/', views.add_score_for, name='add_score_for'),

	path('profile/', views.profile, name='profile'),
	path('profile/view/<int:id>/', views.user_profile, name='user_profile'),
	path('profile/edit/', views.profile_update, name='edit_profile'),
	path('staff/', views.staff_list, name="staff_list"),
	path('staff/add/new/', views.StaffAddView.as_view(), name="add_new_staff"),
	path('staff/edit/<int:pk>/', views.edit_staff, name="edit_staff"),
	path('staff/delete/<int:pk>/', views.delete_staff, name="delete_staff"),
	path('staff/makeadmin/<int:pk>/', views.make_staff_admin, name="make_staff_admin"),
	path('staff/removeadmin/<int:pk>/', views.remove_staff_admin, name="remove_staff_admin"),

	path('courses/', views.course_list, name="course_list"),
	path('courses/add/new', views.CourseAddView.as_view(), name="add_new_course"),
	path('course/delete/<int:pk>/', views.delete_course, name="delete_course"),
	path('course/edit/<int:pk>/', views.course_edit, name="course_edit"),

	path('session/', views.session_list_view, name="manage_session"),
	path('session/add/new', views.session_add_view, name="create_new_session"),
	path('session/edit/<int:pk>/', views.session_update_view, name="edit_session"),
	path('session/delete/<int:pk>/', views.session_delete_view, name="delete_session"),

	path('semester/', views.semester_list_view, name="manage_semester"),
	path('semester/add/new', views.semester_add_view, name="create_new_semester"),
	path('semester/edit/<int:pk>/', views.semester_update_view, name="edit_semester"),
	path('semester/delete/<int:pk>/', views.semester_delete_view, name="delete_semester"),

	path('password/', views.change_password, name='change_password'),

	path('course/assign/', views.CourseAllocationView.as_view(), name='course_allocation'),
	#path('course/registration/', views.course_registration, name='course_registration'),
	path('course/drop/', views.course_drop, name='course_drop'),
	path('course/allocated/', views.course_allocation_view, name='course_allocation_view'),
	path('course/deallocate/<int:pk>/', views.withheld_course, name='withheld_course'),

	path('students/', views.student_list, name="student_list"),
	path('students/<int:pk>/', views.view_student_details, name="student_details"),
	#path('students/<int:pk>/exam_docket/', views.generate_exam_docket, name="generate_exam_docket"),
	path('student/add/new/', views.StudentAddView.as_view(), name="add_new_student"),
	path('student/delete/<int:pk>/', views.delete_student, name="delete_student"),
	path('student/edit/<int:pk>/', views.edit_student, name="edit_student"),
	path('student/course_registration/', views.StudentCourseRegistation.as_view(), name='student_course_registation'),
	# path('students/carry-over-list/', views.carry_over, name='carry_over'),
	# path('students/repeat-list/', views.repeat_list, name='repeat_list'),
	path('students/1st_class_list/', views.first_class_list, name='first_class_list'),
	path('student/result/', views.view_result, name="view_results"),
	path('student/payhistory/', views.pay_history, name='pay_history'),
	path('student/attendance/', views.student_attendance, name='student_attendance'),

	path('parents/', views.parent_list, name='parent_list'),
	path('parents/viewresults/<int:pk>/', views.view_result_by_parent, name='view_result_by_parent'),
	path('parents/paymentshistoryview/<int:pk>/', views.parent_payment_history_view, name='parent_payment_history_view'),
	# path('pdf1/', views.print_pdf, name='html_to_pdf_view1'),
	# path('pdf2/', views.html_to_pdf_view, name='html_to_pdf_view2'),
    #
	# path('result/print/<int:id>/', views.result_sheet_pdf_view, name='result_sheet_pdf_view'),
	# path('registration/form/', views.course_registration_form, name='course_registration_form'),
	path('api/data/', views.get_chart, name='chart'),

	path('managefees/', views.student_fees, name='student_fees'),
	path('managefees/collectfees/', views.FeesCollectionView.as_view(), name='collect_fees'),

	path('manageclasses/', views.manage_classes, name='manage_classes'),
	path('manageclasses/<int:pk>/', views.view_class, name='view_class'),
	path('manageclasses/courses/<int:pk>/', views.get_courses_for_class, name='get_courses_for_class'),
	path('manageclasses/add/new/', views.SchoolClassAddView.as_view(), name="add_new_school_class"),
	path('manageclasses/edit/<int:pk>/', views.class_edit, name="class_edit"),

	path('attendance/classes/', views.student_attendance_list_by_class, name='student_attendance_list_by_class'),
	path('attendance/classes/mark/<int:pk>/', views.student_attendance_mark, name='student_attendance_mark'),
	path('attendance/classes/archive/<int:class_id>/', views.student_attendance_archive, name='student_attendance_archive'),

	path('timetable/all', views.timetable_all, name='timetable_all'),
	path('timetable/by_day', views.timetable_by_day, name='timetable_by_day'),
]