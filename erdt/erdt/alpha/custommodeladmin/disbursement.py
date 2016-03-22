from django.contrib.admin import StackedInline, TabularInline
from financial.models import *
from profiling.models import Profile, University
from globals import ERDTModelAdmin
from django_select2.widgets import *
from suit.widgets import *
from django.forms import ModelForm


class MyForm(ModelForm):
    class Meta:
        fields = '__all__'
        widgets = {
            'budget' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
            'release_date' : SuitDateWidget,
            'description' : AutosizedTextarea(attrs={
                'rows': 4, 
                'class': 'input-xlarge'}),
            'amount' : EnclosedInput(prepend=u'\u20b1',
                attrs={'class': 'input-small'}),
        }


class DisbursementAdmin(ERDTModelAdmin):
    form = MyForm
    list_display = ['release_date', 'line_item', 'amount']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('budget', 'line_item')
        return super(DisbursementAdmin, self).get_readonly_fields(request, obj)

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {
                'fields' : ('budget', 'line_item', 'release_date', 'description', 'amount')
                }
            ),
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if db_field.name == 'budget':
                if my_profile.role == Profile.UNIV_ADMIN:
                    kwargs["queryset"] = Budget.objects.filter(university=my_profile.university.pk)
        except Exception as e:
            print 'Error from DisbursementAdmin.formfield_for_foreignkey:::', e
            kwargs["queryset"] = Budget.objects.none()
        return super(DisbursementAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(DisbursementAdmin, self).get_queryset(request)

        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role == Profile.UNIV_ADMIN:
                return qs.filter(budget__university=my_profile.university.pk)
            elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
                return qs
        except Exception as e:
            print 'Error at DisbursementAdmin:get_queryset:::', e
        return DisbursementAdmin.objects.none()
