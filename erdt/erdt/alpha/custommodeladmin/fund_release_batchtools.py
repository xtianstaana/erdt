from globals import ERDTModelAdmin
from profiling.models import *
from suit.widgets import AutosizedTextarea, EnclosedInput, SuitDateWidget
from django_select2.widgets import Select2Widget
from django.forms import ModelForm


class MyFundReleaseBatchtoolsForm(ModelForm):
    class Meta:
        model = Fund_Release_Batchtools
        fields = '__all__'
        widgets = {
            'description' : AutosizedTextarea(attrs={
                'rows': 4, 
                'class': 'input-xlarge'}),
            'amount_released' : EnclosedInput(prepend=u'\u20b1',
                attrs={'class': 'input-small'}),
            'amount_liquidated' : EnclosedInput(prepend=u'\u20b1',
                attrs={'class': 'input-small'}),
            'date_released' : SuitDateWidget,
            '' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
        }

class FundReleaseBatchtoolsAdmin(ERDTModelAdmin):
    form = MyFundReleaseBatchtoolsForm

    list_display = (
        'date_released', 'line_item', 'amount_released', 'amount_liquidated','description')
    search_fields = ('line_item', 'description', 'university__name', 'university__short_name')

    list_filter = ('line_item', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if db_field.name == 'university':
                qs = University.objects.filter(is_consortium=True)
                if my_profile.role == Profile.UNIV_ADMIN:
                    kwargs["queryset"] = University.objects.filter(pk=my_profile.university.pk)
        except:
            kwargs["queryset"] = University.objects.none()
        return super(FundReleaseBatchtoolsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if obj:
            return (
                ('Scholarship (Local)', {
                    'fields' : ('scholarship_status', 'start_date', 'end_date',)
                    }),
                ('Degree Program', {
                    'fields' : ('university', 'degree_program',)
                    }),
                ('Fund Release', {
                	'fields' : ('line_item', 'date_released', 'amount_released', 'amount_liquidated', 'description')
                    }),
                ('Receipt', {
                	'fields': ('receipt_links',)
                	}),
            )
        return (
            ('Scholarship (Local) Contract Period', {
                'fields' : ('scholarship_status', 'start_date', 'end_date',)
                }),
            ('Degree Program', {
                'fields' : ('university', 'degree_program',)
                }),
            ('Fund Release', {
                'fields' : ('line_item', 'date_released', 'amount_released', 'amount_liquidated', 'description')
                }),
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return (
            	'start_date', 'end_date', 'scholarship_status', 'university', 'degree_program', 
            	'line_item', 'date_released', 'amount_released', 'amount_liquidated', 'description', 
            	'receipt_links',)
        else:
            return super(FundReleaseBatchtoolsAdmin, self).get_readonly_fields(request, obj)

    def get_queryset(self, request):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if  my_profile.role == Profile.UNIV_ADMIN:
                return Fund_Release_Batchtools.objects.filter(
                    university=my_profile.university.id)
            elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
                return Fund_Release_Batchtools.objects.all()
        except Exception as e:
            print 'Error', e
        return Fund_Release_Batchtools.objects.none()