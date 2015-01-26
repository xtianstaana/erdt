"""
Author: Christian Sta.Ana
Date: Sun Aug 10 2014
Description: Contains Admin Customization functions for Person
"""

from globals import ERDTModelAdmin
from django.contrib.admin import StackedInline, TabularInline, HORIZONTAL, VERTICAL
from django import forms
from suit.widgets import *
from django_select2.widgets import Select2Widget
from grants_common import grantStackedInline_factory
from profiling.models import *

class GrantSummaryInline(TabularInline):
    model = Grant
    template = 'admin/edit_inline_with_link/tabular_with_link.html'
    fk_name = 'awardee'
    extra = 0
    verbose_name = 'Grant Awarded'
    verbose_name_plural = 'Grants Awarded'
    suit_classes = 'suit-tab suit-tab-grantsummary'
    fields = ('grant_type', 'start_date', 'end_date', 'allotment', 'total_released', 'total_unexpended',
        'total_unreleased', 'is_active')
    readonly_fields = fields + ('grant_link',)

    def get_fields(self, request, obj=None):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role in (Profile.CENTRAL_OFFICE, Profile.UNIV_ADMIN):
                return (
                    'grant_link', 'start_date', 'end_date', 'allotment', 'total_released', 
                    'total_unexpended','total_unreleased', 'is_active')
        except:
            pass
        return super(GrantSummaryInline, self).get_fields(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False

class ReleaseInline(TabularInline):
    model = Grant_Allocation_Release
    template = 'admin/edit_inline_with_link/tabular_with_link.html'
    fk_name = 'payee'
    extra = 0
    suit_classes = 'suit-tab suit-tab-grantsummary'
    fields = (
        'date_released', 'particular',  'amount_released', 
        'amount_liquidated', 'amount_unexpended')
    readonly_fields = fields + ('release_link',)

    def get_fields(self, request, obj=None):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role in (Profile.CENTRAL_OFFICE, Profile.UNIV_ADMIN):
                return (
                    'date_released', 'release_link',  'amount_released', 
                    'amount_liquidated', 'amount_unexpended')
        except:
            pass
        return super(ReleaseInline, self).get_fields(request, obj)


    def get_max_num(self, request, obj=None, **kwargs):
        if obj:
            try:
                my_profile = Profile.objects.get(person__user=request.user.id, active=True)
                if my_profile.role in (Profile.UNIV_ADMIN, Profile.CENTRAL_OFFICE):
                    if Grant.objects.filter(awardee_id=obj.id).exists():
                        return None
            except:
                pass
        return 0

    def has_delete_permission(self, request, obj=None):
        return False

class EquipmentIssuedInline(TabularInline):
    model = Equipment
    fk_name = 'payee'
    extra = 0
    max_num = 0
    suit_classes = 'suit-tab suit-tab-grantsummary'
    verbose_name = 'Accountable Equipment'
    verbose_name_plural = 'Issued Equipments'
    fields = ('date_released', 'property_no', 'description', 'status', 'accountable')
    readonly_fields = fields + ('description_link', 'accountable_link')

    def get_fields(self, request, obj=None):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role in (Profile.CENTRAL_OFFICE, Profile.UNIV_ADMIN):
                return (
                    'date_released', 'property_no', 'description_link', 'status', 
                    'accountable_link')
        except:
            pass
        return super(EquipmentIssuedInline, self).get_fields(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False

class EquipmentAccountableInline(TabularInline):
    model = Equipment
    fk_name = 'accountable'
    extra = 0
    max_num = 0
    suit_classes = 'suit-tab suit-tab-advisees'
    verbose_name = 'Accountable Equipment'
    verbose_name_plural = 'Accountable Equipments'
    fields = ('date_released', 'property_no', 'description', 'status', 'issued_to')
    readonly_fields = fields + ('description_link',)

    def issued_to(self, obj):
        return obj.payee

    def get_fields(self, request, obj=None):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role in (Profile.CENTRAL_OFFICE, Profile.UNIV_ADMIN):
                return ('date_released', 'property_no', 'description_link', 'status', 'issued_to')
        except:
            pass
        return super(EquipmentAccountableInline, self).get_fields(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False

ScholarshipInline = grantStackedInline_factory(Scholarship, 'suit-tab-scholarship')
SandwichInline = grantStackedInline_factory(Sandwich_Program, 'suit-tab-sandwich')
Scholarship2Inline = grantStackedInline_factory(ERDT_Scholarship_Special, 'suit-tab-scholarship')
FRDGInline = grantStackedInline_factory(FRDG, 'suit-tab-frdg')
FRGTInline = grantStackedInline_factory(FRGT, 'suit-tab-frgt')
PostdocInline = grantStackedInline_factory(Postdoctoral_Fellowship, 'suit-tab-postdoc')
VisitingInline = grantStackedInline_factory(Visiting_Professor_Grant, 'suit-tab-visiting')

class AdviseesInline(TabularInline):
    model = Scholarship
    fk_name = 'adviser'
    verbose_name = 'Advisee'
    verbose_name_plural = 'Advisees'
    fields = (
        'scholar', 'degree_program', 'thesis_status', 'scholarship_status', 'end_date', )
    readonly_fields = fields
    verbose_name_plural = 'Advisees'
    suit_classes = 'suit-tab suit-tab-advisees'
    extra = 0
    max_num = 0

    def scholar(self, obj=None):
        return obj.awardee.my_link()

    def has_delete_permission(self, request, obj=None):
        return False


class EnrolledSubjectInline(TabularInline):
    model = Enrolled_Subject
    fk_name = 'scholar'
    extra = 0
    suit_classes = 'suit-tab suit-tab-enrolled'
    fields = ('subject', 'year_taken', 'eq_grade')
    verbose_name_plural = ''

    def get_readonly_fields(self, request, obj=None):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role in (Profile.UNIV_ADMIN, Profile.CENTRAL_OFFICE):
                return super(EnrolledSubjectInline, self).get_readonly_fields(request, obj)
        except:
            pass
        return ('subject', 'year_taken', 'eq_grade')

class ProfileInline(TabularInline):
    model = Profile
    verbose_name_plural = 'Role and Eligibility'
    verbose_name_plural = 'Roles and Eligibilities'
    exclude = ('active',)
    extra = 0
    suit_classes = 'suit-tab suit-tab-general'

    def get_readonly_fields(self, request, obj=None):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role in (Profile.CENTRAL_OFFICE, Profile.UNIV_ADMIN):
                return super(ProfileInline, self).get_readonly_fields(request, obj)
        except:
            pass
        return ('role', 'university', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            has_central = Profile.objects.filter(
                person__user=request.user.id, role=Profile.CENTRAL_OFFICE).exists()
            if db_field.name == 'university':
                if (my_profile.role == Profile.UNIV_ADMIN) and (not has_central):
                    kwargs["queryset"] = University.objects.filter(pk=my_profile.university.pk)
        except Exception as e:
            print 'Error at ProfileInline', e
        return super(ProfileInline, self).formfield_for_foreignkey(db_field, request, **kwargs)    

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        try:
            if db_field.name == 'role':
                my_profile = Profile.objects.get(person__user=request.user.id, active=True)
                has_central = Profile.objects.filter(
                    person__user=request.user.id, role=Profile.CENTRAL_OFFICE).exists()
                if (my_profile.role == Profile.UNIV_ADMIN) and (not has_central):
                    kwargs['choices'] = Profile.ADMIN_ROLE_CHOICES
        except Exception as e:
            print 'Error at ProfileInline', e
        return super(ProfileInline, self).formfield_for_choice_field(db_field, request, **kwargs)

class MyPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        widgets = {
            'user' : Select2Widget(select2_options={
                'minimumInputLength' : 2,
                'width':'200px'}),
            'address' : AutosizedTextarea(attrs={
                'rows': 4, 
                'class': 'input-xlarge'}),
            'address2' : AutosizedTextarea(attrs={
                'rows': 4, 
                'class': 'input-xlarge'}),
            'birthdate' : SuitDateWidget,
        }

class PersonAdmin(ERDTModelAdmin):
    form = MyPersonForm
    inlines = (
        ProfileInline, AdviseesInline, GrantSummaryInline, ReleaseInline, EquipmentIssuedInline, 
        EquipmentAccountableInline, Scholarship2Inline, ScholarshipInline, SandwichInline, 
        FRGTInline, FRDGInline, PostdocInline, VisitingInline, EnrolledSubjectInline)
    list_display = ('erdt_id', 'name', 'email_address', 'mobile_number', 'user')
    list_display_links = ('name',)
    readonly_fields = ('age', 'erdt_id')
    list_filter = ('profile__role', 'profile__university', )
    search_fields = ('first_name', 'last_name', 'middle_name', 'user__username', 'erdt_id')
    radio_fields =  {'sex' : HORIZONTAL, 'civil_status' : HORIZONTAL}
    fieldsets = (
        ('Personal Information', {
            'classes' : ('suit-tab', 'suit-tab-general',),
            'fields': ('erdt_id', 'photo', 'first_name', 'middle_name', 'last_name', 'sex', 'civil_status',
            'birthdate', 'age')
            }),
        ('Contact Information', {
            'classes' : ('suit-tab', 'suit-tab-general', 'collapse'),
            'fields':('address', 'address2', 'email_address', 'landline_number', 'mobile_number'),
            }),
        ('User Account', {
            'classes' : ('suit-tab', 'suit-tab-general'),
            'fields':('user', ),
            }),
    )

    def get_readonly_fields(self, request, obj=None):
        try:
            my_profile = Profile.objects.get(person__user=request.user.id, active=True)
            if my_profile.role in (Profile.CENTRAL_OFFICE, Profile.UNIV_ADMIN):
                return super(PersonAdmin, self).get_readonly_fields(request, obj)

            if obj and (obj.id==my_profile.person.id) and my_profile.role in (Profile.STUDENT, Profile.ADVISER):
                return (
                    'photo', 'first_name', 'middle_name', 'last_name', 
                    'sex', 'civil_status', 'birthdate', 'user', 'age', 'address', 'erdt_id')
        except:
            pass
        return (
            'photo', 'first_name', 'middle_name', 'last_name', 
            'sex', 'civil_status', 'birthdate', 'user', 'age', 'address', 
            'address2', 'email_address', 'landline_number', 'mobile_number', 'erdt_id')

    def get_suit_form_tabs(self, request, obj=None):
        tabs = [('general', 'General')]
        if obj:
            try:
                profiles = Profile.objects.filter(person__pk=obj.pk)
                is_student_faculty = profiles.filter(role__in=(Profile.STUDENT, Profile.ADVISER, Profile.VISITING)).exists()

                grants = Grant.objects.filter(awardee__pk=obj.pk)

                if Scholarship.objects.filter(adviser__pk=obj.pk).exists() or Equipment.objects.filter(accountable__pk=obj.pk).exists():
                    tabs.append(('advisees', 'Accountabilities'), )

                if grants.exists() or is_student_faculty:
                    tabs.append(('grantsummary', 'Grants Summary'))
                
                if grants.instance_of(Scholarship).exists() or grants.instance_of(ERDT_Scholarship_Special).exists():
                    tabs.append(('scholarship', 'Scholarships'))
                if grants.instance_of(Sandwich_Program).exists():
                    tabs.append(('sandwich', 'Sandwich'))
                if grants.instance_of(FRGT).exists():
                    tabs.append(('frgt', 'FRGs'))
                if grants.instance_of(FRDG).exists():
                    tabs.append(('frdg', 'FRDGs'))
                if grants.instance_of(Postdoctoral_Fellowship).exists():
                    tabs.append(('postdoc', 'Postdoc'))
                if grants.instance_of(Visiting_Professor_Grant).exists():
                    tabs.append(('visiting', 'Visiting Prof'))

                if grants.instance_of(Scholarship).exists():
                    tabs.append(('enrolled', 'Enrolled Subjects'))
            except:
                pass
        return tabs
    
    """
    Author: Christian Sta.Ana
    Date: Sun Sep 28 2014
    Description: Setting row/record-level permissions.
    Params: default
    Returns: default
    """
    def get_queryset(self, request):
        try:
            my_profile = Profile.objects.filter(person__user=request.user.id, active=True)
            if my_profile.exists():
                my_profile = my_profile[0]
            else:
                return Person.objects.filter(user__pk=request.user.pk)

            if my_profile.role == Profile.STUDENT:
                return Person.objects.filter(user__pk=request.user.pk)
            elif my_profile.role == Profile.ADVISER:
                iam = Person.objects.filter(user__pk=request.user.pk)
                advisees = Person.objects.filter(grants__in=iam[0].advisees.all())
                return (iam|advisees).distinct()
            elif my_profile.role == Profile.UNIV_ADMIN: # If User's profile is UNIV_ADMIN
                return Person.objects.filter(
                    Q(profile__university__pk=my_profile.university.pk)|Q(profile__isnull=True)
                    ).distinct()
            elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
                return Person.objects.all()
        except Exception as e:
            print 'Error at PersonAdmin', e
        return Person.objects.none()
