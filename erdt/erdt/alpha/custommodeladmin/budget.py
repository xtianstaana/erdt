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
    model = LineItem
    fk = 'budget'
    extra = 0
    form = LineItemInlineForm
    suit_classes = 'suit-tab suit-tab-general'
    verbose_name_plural = ''


class MyForm(ModelForm):
    class Meta:
        fields = '__all__'
        widgets = {
            'university' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
            'start_date' : SuitDateWidget,
            'end_date' : SuitDateWidget,
        }


class BudgetAdmin(ERDTModelAdmin):
    form = MyForm
    inlines = [LineItemInline]
    list_display = ['period', 'university', 'total_budget']
    readonly_fields = ('total_budget', 'release_scholarship_local', 'release_sandwich')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('university', 'total_budget', 'release_scholarship_local', 'release_sandwich')
        return super(BudgetAdmin, self).get_readonly_fields(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):    
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if db_field.name == 'university':
                qs = University.objects.filter(is_consortium=True)
                if my_profile.role == Profile.UNIV_ADMIN:
                    kwargs["queryset"] = University.objects.filter(pk=my_profile.university.pk)
        except Exception as e:
            print 'Error from BudgetAdmin.formfield_for_foreignkey:::', e
            kwargs["queryset"] = University.objects.none()
        return super(BudgetAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(BudgetAdmin, self).get_queryset(request)

        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role == Profile.UNIV_ADMIN:
                return qs.filter(university=my_profile.university.pk)
            elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
                return qs
        except Exception as e:
            print 'Error at BudgetAdmin:get_queryset:::', e
        return Budget.objects.none()

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {
                'classes' : ('suit-tab', 'suit-tab-general'),
                'fields' : ('university', 'start_date', 'end_date', 'total_budget')
                }
            ),
            (None, {
                'classes': ('suit-tab', 'suit-tab-releases'),
                'fields': ('release_scholarship_local', 'release_sandwich') 
                }
            )
        )

    def get_suit_form_tabs(self, request, obj=None):
        tabs = [('general', 'General')]
        if obj:
            tabs.append(('releases', 'Release Summary'))
        return tabs
