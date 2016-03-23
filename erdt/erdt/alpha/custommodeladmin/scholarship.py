"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for Scholarship
"""

from globals import ERDTModelAdmin
from django.db import models
from django.contrib.admin import StackedInline, TabularInline, actions
from django.forms import ModelForm
from django.forms.widgets import *
from suit.widgets import *
from django_select2.widgets import *

# Import Profiling Module Models 
from profiling.models import *

from django.http import HttpResponseRedirect, HttpResponse
from grants_common import *
import csv

class MyScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = '__all__'
        widgets = {
            'awardee' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
            'description' : AutosizedTextarea(attrs={
                'rows': 4, 
                'class': 'input-xlarge'}),
            'thesis_title' : AutosizedTextarea(attrs={
                'rows': 4, 
                'class': 'input-xlarge'}),
            'thesis_topic' : AutosizedTextarea(attrs={
                'rows': 4, 
                'class': 'input-xlarge'}),
            'start_date' : SuitDateWidget,
            'end_date' : SuitDateWidget,
            'entry_grad_program' : SuitDateWidget,
            'end_grad_program' : SuitDateWidget,
            'ce_schedule' : SuitDateWidget,
            'adviser' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
            'high_degree_univ' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
        }

from django.contrib.admin import SimpleListFilter, DateFieldListFilter
from django.utils.translation import ugettext_lazy as _


class ProgramFilter(SimpleListFilter):
    title = _('program')
    parameter_name = 'program'

    def lookups(self, request, model_admin):
        try:
            q = Degree_Program.objects.order_by('program').values_list('program').distinct()
        except:
            q = ('',)

        return tuple((c[0], c[0]) for c in q)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(degree_program__program=self.value())
        else:
            return queryset

class ScholarshipAdmin(ERDTModelAdmin):
    form = MyScholarshipForm
    inlines = [
        lineItemInline_factory(Grant_Allocation.SCHOLARSHIP_ALLOC_CHOICES), 
        ReleaseSummaryInline, ReleaseInline]
    list_display = ('awardee', 'email', 'degree_program', 'start_date', 'end_date', 'adviser')
    list_filter = (
        'university', 'degree_program__degree', ProgramFilter,
        'scholarship_status')
    actions = ('export_csv',)
    search_fields = ('start_date',)
    list_max_show_all = 10000000

    readonly_fields = ('awardee_link',)

    def get_search_results(self, request, queryset, search_term):
        if search_term:
            try:
                start_date, end_date = search_term.split()
                return queryset.filter(start_date__gte=start_date, end_date__lte=end_date), True
            except Exception as e:
                return Scholarship.objects.none(), True
        else:
            return queryset, False

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename="scholar_list.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ERDT Scholarship (Local) List'])
        writer.writerow([])
        writer.writerow(['Name', 'Email', 'Degree Program', 'Scholarship Status', 'Start Date', 'End Date', 'Lateral', 'Adviser'])
        for q in queryset:
            write = [
                q.awardee.__str__(),
                q.awardee.email_address,
                q.degree_program.__str__(),
                q.get_scholarship_status_display(),
                q.start_date.__str__(),
                q.end_date.__str__(),
                q.lateral
                ]
            if q.adviser:
                write.append(q.adviser.__str__())
            writer.writerow(write)
        return response

    export_csv.short_description = 'Export selected Scholarship (Local) to CSV'

    def get_fieldsets(self, request, obj=None):
        awardee = 'awardee'
        if obj:
            awardee = 'awardee_link'
        return (
            (None, {
                'classes' : ('suit-tab', 'suit-tab-general'),
                'fields' : (awardee, 'start_date', 'end_date', 'description', 
                            'scholarship_status'),
                }),
            ('Program Detail', {
                'classes' : ('suit-tab', 'suit-tab-general'),
                'fields' : ('university', 'degree_program', 'entry_grad_program' , 
                            'end_grad_program', 'ce_schedule',
                    'lateral', 'cleared'),
                }),
            ('Educational Background', {
                'classes' : ('suit-tab', 'suit-tab-general'),
                'fields' : ('high_degree_univ', 'high_degree'),
                }),
            (None, {
                'classes' : ('suit-tab', 'suit-tab-thesis'),
                'fields' : ('adviser', 'thesis_status', 'thesis_title', 'thesis_topic'),
                }),
            ('Exportable CSVs', {
                'classes' : ('suit-tab', 'suit-tab-releases'),
                'fields' : ('grant_financial_release_link',)
                })
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('awardee_link', 'university', 'record_manager', 'degree_program', 'grant_financial_release_link')
        return super(ScholarshipAdmin, self).get_readonly_fields(request, obj)

    def get_suit_form_tabs(self, request, obj=None):
        tabs = [('general', 'General'), ('thesis', 'Thesis / Dissertation Information'), 
        ('allocation', 'Line Item Budget')]

        if obj:
            tabs.append(('releases', 'Release Summary'))
        return tabs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if db_field.name == 'awardee':
                qs = Person.objects.filter(profile__role=Profile.STUDENT)
                if my_profile.role == Profile.UNIV_ADMIN:
                    qs = qs.filter(profile__university__pk=my_profile.university.pk)
                kwargs["queryset"] = qs.distinct()
            elif db_field.name == 'university':
                if my_profile.role == Profile.UNIV_ADMIN:
                    kwargs["queryset"] = University.objects.filter(pk=my_profile.university.pk)
            elif db_field.name == 'adviser':
                qs = Person.objects.filter(profile__role=Profile.ADVISER)
                if my_profile.role == Profile.UNIV_ADMIN:
                    qs = qs.filter(profile__university__pk=my_profile.university.pk)
                kwargs["queryset"] = qs.distinct()
        except:
            kwargs["queryset"] = Person.objects.none()
        return super(ScholarshipAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)

            if my_profile.role == Profile.UNIV_ADMIN: # If User's profile is UNIV_ADMIN
                return Scholarship.objects.filter(record_manager__pk=my_profile.university.pk)
            elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
                return Scholarship.objects.all()
        except Exception as e:
            print 'Error at ScholarshipAdmin', e
        return Scholarship.objects.none()

    def save_model(self, request, obj, form, change):
        if not (obj.id and obj.record_manager):
            obj.record_manager = obj.university
        super(ScholarshipAdmin, self).save_model(request, obj, form, change)