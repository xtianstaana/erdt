from django.contrib.admin import StackedInline, TabularInline
from profiling.models import Grant, Grant_Allocation, Grant_Allocation_Release, Person, Profile, University
from django.forms import ModelForm
from suit.widgets import AutosizedTextarea, EnclosedInput, SuitDateWidget
from django_select2.widgets import Select2Widget

from globals import ERDTModelAdmin


def grantStackedInline_factory(my_grant, my_tab):
	class GrantInline(StackedInline):
		model = my_grant
		fk_name = 'awardee'
		extra = 0
		max_num = 0
		other_fields = tuple(
			fld.name for fld in my_grant._meta.fields 
				if (fld not in Grant._meta.fields) and fld.name != 'grant_ptr')

		fields = ('start_date', 'end_date',  'description') + other_fields + ('allocation_summary',)
		readonly_fields = fields
		verbose_name_plural = ''
		suit_classes = 'suit-tab %s' % my_tab

		def has_delete_permission(self, request, obj=None):
			return False

		def show_url(self, instance):
			return True

	return GrantInline

def grantModelAdmin_factory(my_grant, choices, *eligible):
	class GrantForm(ModelForm):
		class Meta:
			model = my_grant
			fields = '__all__'
			widgets = {
				'awardee' : Select2Widget(select2_options={
					'minimumInputLength' : 2,
					'width':'200px'}),
				'description' : AutosizedTextarea(attrs={
					'rows': 4, 
					'class': 'input-xlarge'}),
				'start_date' : SuitDateWidget,
				'end_date' : SuitDateWidget,
				'record_manager' : Select2Widget(select2_options={
					'minimumInputLength' : 2,
					'width':'200px'}),
			}

	class GrantModelAdmin(ERDTModelAdmin):
		LineItemInline = lineItemInline_factory(choices)

		form = GrantForm
		inlines =[LineItemInline, ReleaseSummaryInline, ReleaseInline]
		list_display = ('awardee', 'start_date', 'end_date', )
		search_fields = ('awardee__first_name', 'awardee__last_name', 'awardee__middle_name', 'awardee__erdt_id')

		def get_readonly_fields(self, request, obj=None):
			_ro = super(GrantModelAdmin,self).get_readonly_fields(request, obj)
			_mro = ('awardee_link', 'record_manager', )
			try:
				my_profile = Profile.objects.get(person__user=request.user.id, active=True)
				if my_profile.role == Profile.CENTRAL_OFFICE:
					_mro = ('awardee_link',)
			except:
				pass
			if _ro:
				return tuple(_ro) + _mro
			return _mro


		def get_fieldsets(self, request, obj=None):
			awardee = 'awardee'	
			other_fields = tuple(fld.name for fld in self.model._meta.fields 
				if (fld not in Grant._meta.fields) and fld.name != 'grant_ptr')

			others = (('Other Information', {
					'classes' : ('suit-tab', 'suit-tab-general'),
					'fields' : other_fields
				}),) if other_fields else tuple()

			if obj:
				awardee = 'awardee_link'
			return (
				(None, {
					'classes' : ('suit-tab', 'suit-tab-general'),
					'fields' : (awardee, 'start_date', 'end_date', 'description', 'record_manager')
				}),
			) + others

		def formfield_for_foreignkey(self, db_field, request, **kwargs):
			is_person = 0
			try:
				my_profile = Profile.objects.get(person__user=request.user.id, active=True)
				if db_field.name == 'awardee':
					is_person = 1
					qs = Person.objects.filter(profile__role__in=tuple(eligible))
					if my_profile.role == Profile.UNIV_ADMIN:
						qs = qs.filter(profile__university__pk=my_profile.university.pk)
					kwargs["queryset"] = qs.distinct()
				elif db_field.name == 'host_univesity':
					is_person = 2
					qs = University.objects.filter(is_consortium=True)
					if my_profile.role == Profile.UNIV_ADMIN:
						qs = qs.filter(pk=my_profile.university.pk)
					kwargs["queryset"] = qs
				elif db_field.name == 'host_professor':
					is_person = 1
					qs = Person.objects.filter(profile__role=Profile.ADVISER)
					if my_profile.role == Profile.UNIV_ADMIN:
						qs = qs.filter(profile__university__pk=my_profile.university.pk)
					kwargs["queryset"] = qs.distinct()
			except Exception as e:
				print 'Error from GrantModelAdmin.formfield_for_foreignkey:::', e
				if is_person == 1:
					kwargs["queryset"] = Person.objects.none()
				elif is_person == 2:
					kwargs["queryset"] = University.objects.none()
			return super(GrantModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

		def get_suit_form_tabs(self, request, obj=None):
			tabs = [('general', 'General'), ('allocation', 'Line Item Budget')]

			if obj:
				tabs.append(('releases', 'Release Summary'))
			return tabs

		def save_model(self, request, obj, form, change):
			if not obj.id:
				obj.record_manager = Profile.objects.get(person__user=request.user.id, active=True).university
			super(GrantModelAdmin, self).save_model(request, obj, form, change)

		def get_queryset(self, request):
			qs = super(GrantModelAdmin, self).get_queryset(request)

			try:
				my_profile = Profile.objects.get(person__user=request.user.id, active=True)
				if my_profile.role == Profile.UNIV_ADMIN:
					qs = qs.filter(record_manager__pk=my_profile.university.pk)
				elif my_profile.role in (Profile.CENTRAL_OFFICE, Profile.DOST):
					return qs
			except Exception as e:
				print 'Error at GrantModelAdmin:get_queryset:::', e
			return Grant.objects.none()

	return GrantModelAdmin

def lineItemInline_factory(choices):
	class MyForm(ModelForm):
		class Meta:
			fields = '__all__'
			widgets = {
				'amount' : EnclosedInput(prepend=u'\u20b1',
					attrs={'class': 'input-small'}),
			}

	class _LineItemInline(TabularInline):
		form = MyForm
		model = Grant_Allocation
		fk_name = 'grant'
		extra = 0
		max_num = len(choices)
		suit_classes = 'suit-tab suit-tab-allocation'
		verbose_name_plural = ''

		def formfield_for_choice_field(self, db_field, request, **kwargs):
			if db_field.name == 'name':
				kwargs['choices'] = choices
			return super(_LineItemInline, self).formfield_for_choice_field(db_field, request, **kwargs)
	return _LineItemInline

class ReleaseInline(TabularInline):
	model = Grant_Allocation_Release
	fk = 'grant'
	extra = 0
	max_num = 0
	fields =  ('date_released', 'release_link',  'amount_released', 'amount_liquidated', 'amount_unexpended')
	readonly_fields = fields
	suit_classes = 'suit-tab suit-tab-releases'

	def has_delete_permission(self, request, obj=None):
		return False

class ReleaseSummaryInline(TabularInline):
	model = Grant_Allocation
	fk = 'grant'
	extra = 0
	max_num = 0
	verbose_name_plural = ''
	fields =  ('name', 'approved_budget', 'total_released', 'total_expenditure', 'total_unexpended', 'total_unreleased')
	readonly_fields = fields
	suit_classes = 'suit-tab suit-tab-releases'

	def approved_budget(self, obj=None):
		if obj:
			return obj.amount
		return 0.0

	def has_delete_permission(self, request, obj=None):
		return False
