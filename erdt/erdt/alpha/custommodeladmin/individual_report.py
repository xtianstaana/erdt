from erdt.alpha.custommodeladmin.globals import ERDTModelAdmin
from reporting.models import Individual_Report
from profiling.models import Person, Profile
from django_select2.widgets import *

class MyIndividualReportForm(forms.ModelForm):
    class Meta:
        model = Individual_Report
        fields = '__all__'
        widgets = {
            'person' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
            }

class IndividualReportAdmin(ERDTModelAdmin):
    form = MyIndividualReportForm
    exclude = ('active_only',)
    fields = ('person', 'name', 'report_type', 'start_date', 'end_date', 'description', )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.fields + ('report_link',)
        return super(IndividualReportAdmin, self).get_readonly_fields(request, obj)

    def get_fields(self, request, obj=None):
        if obj:
            return self.fields + ('report_link',)
        return super(IndividualReportAdmin, self).get_fields(request, obj)

    def get_change_form_template(self, request, obj=None):
        if obj:
            return 'admin/reporting/change_form_pdf.html'
        return super(IndividualReportAdmin, self).get_change_form_template(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'person':
            try:
                my_profile = Profile.objects.get(person__user=request.user.id, active=True)

                if my_profile.role == Profile.UNIV_ADMIN: # If User's profile is UNIV_ADMIN
                    kwargs["queryset"] = Person.objects.filter(
                        Q(profile__university__pk=my_profile.university.pk)|Q(profile__isnull=True)
                        ).distinct()
                elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
                    kwargs["queryset"] = Person.objects.all()
            except Exception as e:
                kwargs["queryset"] = Person.objects.none()        
        return super(IndividualReportAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
