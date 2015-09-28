from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader, Context
from wkhtmltopdf.views import *
from reporting.models import *
from profiling.models import *
import csv

@login_required
def create_university_report_pdf(request, university_report_id):

    report = University_Report.objects.get(pk=university_report_id)

    context = {'report' : report.create_report}

    return PDFTemplateResponse(request, 'admin/reporting/change_form_pdf.html', context, 'test.pdf', 200, footer_template='admin/reporting/footer.html', header_template='admin/reporting/header.html')

@login_required
def create_individual_report_pdf(request, individual_report_id):

    report = Individual_Report.objects.get(pk=individual_report_id)

    context = {'report' : report.create_report}

    return PDFTemplateResponse(request, 'admin/reporting/change_form_pdf.html', context, 'test.pdf', 200, footer_template='admin/reporting/footer.html', header_template='admin/reporting/header.html')

@login_required
def create_list_advisees(request, faculty_id):
    my_profile = Profile.objects.filter(person__user=request.user.id, active=True)
    
    f_profile = Profile.objects.filter(person__pk=faculty_id, role=Profile.ADVISER)
    default = HttpResponse("You do not have the right permission to perform this action. This incident has been reported.", content_type="text/plain")
    default2 = HttpResponse("dfd", content_type="text/plain")

    if my_profile.exists() and f_profile.exists():
        my_profile = my_profile[0]
        f_profile = f_profile[0]

        if ((my_profile.role == Profile.UNIV_ADMIN) and (my_profile.university == f_profile.university)) or my_profile.role == Profile.CENTRAL_OFFICE:
            faculty = Person.objects.get(pk=faculty_id)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment;filename="%s.csv"' % ('ERDT ADVISEES - ' + faculty.name())

            writer = csv.writer(response)
            writer.writerow(['ERDT Faculty Adviser:', faculty.__str__()])
            writer.writerow([])
            writer.writerow(['Scholar', 'Email Address', 'Scholarship Status', 'Degree Program', 'Lateral?', 'Start Date', 'End Date', 'Date of Graduation'])

            for sch in faculty.advisees.all():
                try:
                    writer.writerow([
                        sch.awardee.__str__(), 
                        sch.awardee.email_address, 
                        sch.get_scholarship_status_display(), 
                        sch.degree_program.__unicode__(),
                        sch.lateral,
                        sch.start_date.isoformat(),
                        sch.end_date.isoformat(),
                        sch.end_grad_program.isoformat()])
                except:
                    pass

            return response
    return default

