from django.conf import settings
from django.shortcuts import render

# Create your views here.
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from weasyprint import HTML
from django.template.loader import render_to_string
from school.models import Student, SchoolFees, Timetable, User, SchoolDetails


# Create your views here.
def staff_list_report(request):
    schooldetails = SchoolDetails.objects.all()
    staff = User.objects.filter(is_student=False, is_parent=False)
    html_string = render_to_string('reports/staff_list_report.html',
                                   {
                                       'staff': staff,
                                       'schooldetails': schooldetails,
                                   })

    html = HTML(string=html_string, base_url=request.build_absolute_uri())


    html.write_pdf(target='/tmp/mypdf.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Staff List Report.pdf"'
        return response
        #return FileResponse('', as_attachment=False, content_type='application/pdf', filename='hello.pdf')

    return response


def students_list_report(request):
    schooldetails = SchoolDetails.objects.all()
    students = Student.objects.all()
    html_string = render_to_string('reports/students_list_report.html',
                                   {
                                       'students': students,
                                       'schooldetails': schooldetails,
                                   })

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    html.write_pdf(target='/tmp/mypdf.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response
        #return FileResponse('', as_attachment=False, content_type='application/pdf', filename='hello.pdf')

    return response


def payments_list_report(request):
    schooldetails = SchoolDetails.objects.all()
    schoolfees = SchoolFees.objects.all()
    total = 0
    for t in schoolfees:
        total += t.amountpaid
    html_string = render_to_string('reports/payments_list_report.html',
                                   {
                                       'schoolfees': schoolfees,
                                       'total': total,
                                       'schooldetails': schooldetails,
                                   })

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    html.write_pdf(target='/tmp/payments_report.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('payments_report.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="payments_report.pdf"'
        return response
        #return FileResponse('', as_attachment=False, content_type='application/pdf', filename='hello.pdf')

    return response


def payments_history_report(request):
    schooldetails = SchoolDetails.objects.all()

    if request.user.is_student:
        schoolfees = SchoolFees.objects.filter(student__user_id__exact=request.user.id)
        total = 0
        for t in schoolfees:
            total += t.amountpaid
        html_string = render_to_string('reports/payment_history_report.html',
                                       {
                                           'schoolfees': schoolfees,
                                           'total': total,
                                           'schooldetails': schooldetails,
                                       })

        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/payments_history_report.pdf')

        fs = FileSystemStorage('/tmp')
        with fs.open('payments_history_report.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="payments_history_report.pdf"'
            return response
            #return FileResponse('', as_attachment=False, content_type='application/pdf', filename='hello.pdf')

        return response


def timetable_all_report(request):
    schooldetails = SchoolDetails.objects.all()
    timetables = Timetable.objects.all()
    html_string = render_to_string('reports/timetable_all_report.html',
                                   {
                                       'timetables': timetables,
                                       'schooldetails': schooldetails,
                                   })

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    html.write_pdf(target='/tmp/timetable_all_report.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('timetable_all_report.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="timetable_all_report.pdf"'
        return response
        #return FileResponse('', as_attachment=False, content_type='application/pdf', filename='hello.pdf')

    return response


