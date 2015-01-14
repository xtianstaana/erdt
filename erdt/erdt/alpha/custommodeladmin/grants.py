from grants_common import grantModelAdmin_factory
from profiling.models import Grant_Allocation, Profile, FRDG, FRGT, \
	Postdoctoral_Fellowship, Sandwich_Program, ERDT_Scholarship_Special, \
	Visiting_Professor_Grant

FRGTAdmin = grantModelAdmin_factory(FRGT, Grant_Allocation.FRGT_ALLOC_CHOICES, Profile.ADVISER)
FRDGAdmin = grantModelAdmin_factory(FRDG, Grant_Allocation.FRDG_ALLOC_CHOICES, Profile.ADVISER)
PostdoctoralAdmin = grantModelAdmin_factory(Postdoctoral_Fellowship, 
	Grant_Allocation.POSTDOCTORAL_ALLOC_CHOICES, Profile.ADVISER)
SandwichAdmin = grantModelAdmin_factory(Sandwich_Program, 
	Grant_Allocation.SANDWICH_ALLOC_CHOICES, Profile.ADVISER, Profile.STUDENT)
Scholarship2Admin = grantModelAdmin_factory(ERDT_Scholarship_Special, 
	Grant_Allocation.SCHOLARSHIP2_ALLOC_CHOICES, Profile.ADVISER)
_VisitingProfessorAdmin = grantModelAdmin_factory(Visiting_Professor_Grant, 
	Grant_Allocation.VP_ALLOC_CHOICES, Profile.VISITING)


from django.forms import ModelForm
from django_select2.widgets import Select2Widget
from suit.widgets import AutosizedTextarea, EnclosedInput, SuitDateWidget

class MyVisitingProfessorForm(ModelForm):
	class Meta:
		model = Visiting_Professor_Grant
		fields = '__all__'
		widgets = {
			'awardee' : Select2Widget(select2_options={
				'minimumInputLength' : 2,
				'width':'200px'}),
			'description' : AutosizedTextarea(attrs={
				'rows': 4, 
				'class': 'input-xlarge'}),
			'allotment' : EnclosedInput(prepend=u'\u20b1'),
			'start_date' : SuitDateWidget,
			'end_date' : SuitDateWidget,
			'host_university' : Select2Widget(select2_options={
				'minimumInputLength' : 2,
				'width':'200px'}),
			'host_professor' : Select2Widget(select2_options={
				'minimumInputLength' : 2,
				'width':'200px'}),
			'record_manager' : Select2Widget(select2_options={
					'minimumInputLength' : 2,
					'width':'200px'}),
		}

class VisitingProfessorAdmin(_VisitingProfessorAdmin):
	form = MyVisitingProfessorForm

	def get_readonly_fields(self, request, obj=None):
		_ro = super(VisitingProfessorAdmin, self).get_readonly_fields(request, obj)
		_mro = ('host_university',)
		if obj:
			return tuple(_ro) + _mro
		return _ro