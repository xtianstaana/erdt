from erdt.alpha.custommodeladmin.globals import ERDTModelAdmin
from reporting.models import University_Report
from profiling.models import University, Profile
from django_select2.widgets import *


class MyUniversityReportForm(forms.ModelForm):
    class Meta:
        model = University_Report
        fields = '__all__'
        widgets = {
            'university' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
            }

class UniversityReportAdmin(ERDTModelAdmin):
    form = MyUniversityReportForm
    exclude = ('active_only',)
    fields = ('university', 'name', 'report_type', 'start_date', 'end_date', 'description', )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.fields + ('report_link',)
        return super(UniversityReportAdmin, self).get_readonly_fields(request, obj)

    def get_fields(self, request, obj=None):
        if obj:
            return self.fields + ('report_link',)
        return super(UniversityReportAdmin, self).get_fields(request, obj)

    def get_change_form_template(self, request, obj=None):
        if obj:
            return 'admin/reporting/change_form_pdf.html'
        return super(UniversityReportAdmin, self).get_change_form_template(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'university':
            try:
                my_profile = Profile.objects.get(person__user=request.user.id, active=True)

                if my_profile.role == Profile.UNIV_ADMIN: # If User's profile is UNIV_ADMIN
                    kwargs["queryset"] = University.objects.filter(pk=my_profile.university.pk)
                elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
                    kwargs["queryset"] = University.objects.all()
            except Exception as e:
                kwargs["queryset"] = University.objects.none()        
        return super(UniversityReportAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)