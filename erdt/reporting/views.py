from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Context
from wkhtmltopdf.views import *
from reporting.models import *


def create_university_report_pdf(request, university_report_id):

    report = University_Report.objects.get(pk=university_report_id)

    context = {'report' : report.create_report}

    return PDFTemplateResponse(request, 'admin/reporting/change_form_pdf.html', context, 'test.pdf', 200, footer_template='admin/reporting/footer.html', header_template='admin/reporting/header.html')


def create_individual_report_pdf(request, individual_report_id):

    report = Individual_Report.objects.get(pk=individual_report_id)

    context = {'report' : report.create_report}

    return PDFTemplateResponse(request, 'admin/reporting/change_form_pdf.html', context, 'test.pdf', 200, footer_template='admin/reporting/footer.html', header_template='admin/reporting/header.html')


