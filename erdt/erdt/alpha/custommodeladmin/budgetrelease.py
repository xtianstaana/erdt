from django.contrib.admin import StackedInline, TabularInline
from financial.models import *
from profiling.models import Profile, University
from globals import ERDTModelAdmin
from django_select2.widgets import *
from suit.widgets import *
from django.forms import ModelForm


class LineItemInlineForm(ModelForm):
    class Meta:
        fields = '__all__'
        widgets = {
            'description' : AutosizedTextarea(attrs={
                'rows': 4, 
                'class': 'input-xlarge'
            }),
            'amount' : EnclosedInput(prepend=u'\u20b1',
                attrs={'class': 'input-small'}),
            
        }  


class LineItemInline(TabularInline):
    parent_obj = None
    model = LineItemBudgetRelease
    fk = 'budget_release'
    extra = 0
    form = LineItemInlineForm
    verbose_name_plural = ''

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            if db_field.name == 'line_item':
                if self.parent_obj is None:
                    kwargs["queryset"] = LineItem.objects.none()
                else:
                    kwargs["queryset"] = LineItem.objects.filter(budget=self.parent_obj.budget.pk)
        except Exception as e:
            print 'Error from LineItemInline.formfield_for_foreignkey:::', e
            kwargs["queryset"] = LineItem.objects.none()
        return super(LineItemInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super(LineItemInline, self).get_formset(request, obj, **kwargs)

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
        }


class BudgetReleaseAdmin(ERDTModelAdmin):
    form = MyForm
    inlines = [LineItemInline]
    list_display = ['release_date', 'description', 'total_amount']
    readonly_fields = ('total_amount',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('budget', 'total_amount')
        return super(BudgetReleaseAdmin, self).get_readonly_fields(request, obj)

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {
                'fields' : ('budget', 'release_date', 'description', 'total_amount')
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
            print 'Error from BudgetReleaseAdmin.formfield_for_foreignkey:::', e
            kwargs["queryset"] = Budget.objects.none()
        return super(BudgetReleaseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(BudgetReleaseAdmin, self).get_queryset(request)

        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role == Profile.UNIV_ADMIN:
                return qs.filter(budget__university=my_profile.university.pk)
            elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
                return qs
        except Exception as e:
            print 'Error at BudgetReleaseAdmin:get_queryset:::', e
        return BudgetRelease.objects.none()
