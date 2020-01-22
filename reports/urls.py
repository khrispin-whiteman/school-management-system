from django.urls import path

from reports import views

urlpatterns = [
    path('students/report/', views.students_list_report, name='students_list_report'),
    path('staff/report/', views.staff_list_report, name='staff_list_report'),
    path('finance/report/', views.payments_list_report, name='payments_list_report'),
    path('payments_history/report/', views.payments_history_report, name='payments_history_report'),
    path('timetable/all/report/', views.timetable_all_report, name='timetable_all_report'),
]