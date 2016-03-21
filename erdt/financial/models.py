from django.db import models
from django.db.models import PROTECT, Sum
from polymorphic import PolymorphicModel
from datetime import datetime, date
from smart_selects.db_fields import ChainedForeignKey as GF
from profiling import models as profiling_models
from django.core.exceptions import ValidationError


class Budget(models.Model):
    university = models.ForeignKey(
        profiling_models.University, 
        limit_choices_to={'is_consortium':True}, 
        on_delete=PROTECT)
    start_date = models.DateField(verbose_name='Start of period', help_text='Format: YYYY-MM-DD')
    end_date = models.DateField(verbose_name='End of period', help_text='Format: YYYY-MM-DD')

    class Meta:
        verbose_name = 'Line Item Budget'
        verbose_name_plural = 'Line Item Budget'

    def release_scholarship_local(self):
        out = u'<tr> <td><b>Line Item</b></td> <td><b>Budget</b></td>  \
            <td><b>Released</b></td> <td><b>Unexpended</b></td> <td><b>Unreleased</b></td> </tr>'

        _temp =  '<td> %s </td>' + ('<td class="numeric"> %s </td> ' * 4)

        t_allotment, t_released, t_unexpended, t_unreleased = (0.0, 0.0, 0.0, 0.0)

        
        # for allocation in self.grant_allocation_set.all():


    def total_budget(self):
        total_amount = self.lineitem_set.aggregate(Sum('amount')).values()[0]
        return '{:,.2f}'.format(total_amount) if total_amount else '0.00'
    total_budget.short_description = 'Budget'

    def period(self):
        start = self.start_date.strftime('%b')
        end = self.end_date.strftime('%b')
        return '%s-%s %s' % (start, end, self.start_date.year)

    def __unicode__(self):
        return '%s: %s' % (self.university, self.period())

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('Start of period date must precede or the same as the end of period date.')
        if self.start_date.year != self.end_date.year:
            raise ValidationError('Start and end period year must be the same.')


class LineItem(models.Model):
    ITEM_CHOICES = (
        ('Traveling (Conference/Summit)', 'Traveling (Conference/Summit)'),
        ('Printing and Binding (Reports/Directory)', 'Printing and Binding (Reports/Directory)'),
        ('Scholarship (Local): Tuition and Fees', 'Scholarship (Local): Tuition and Fees'),
        ('Scholarship (Local): Stipends', 'Scholarship (Local): Stipends'),
        ('Scholarship (Local): Book Allowance', 'Scholarship (Local): Book Allowance'),
        ('Scholarship (Local): Transportation Allowance', 'Scholarship (Local): Transportation Allowance'),
        ('Scholarship (Local): Thesis/Dissertation Allowance', 'Scholarship (Local): Thesis/Dissertation Allowance'),
        ('Scholarship (Local): Research Grant', 'Scholarship (Local): Research Grant'),
        ('Scholarship (Local): Research Dissemination Allowance', 'Scholarship (Local): Research Dissemination Allowance'),
        ('Scholarship (Local): Mentor\'s Fee', 'Scholarship (Local): Mentor\'s Fee'),
        ('Sandwich Program', 'Sandwich Program'),
        ('Scholarship (PhD Abroad)', 'Scholarship (PhD Abroad)'),
        ('Postdoctoral Fellowships', 'Postdoctoral Fellowships'),
        ('Faculty Research Grant', 'Faculty Research Grant'),
        ('Faculty Research Dissemination Grant', 'Faculty Research Dissemination Grant'),
        ('Visiting Professors', 'Visiting Professors'),
        ('Visiting Professors (Distinguished)', 'Visiting Professors (Distinguished)'),
        ('Online Research Resources', 'Online Research Resources'),
        ('Conference and Summit Expenses', 'Conference and Summit Expenses'),
        ('Training Programs and Workshops', 'Training Programs and Workshops'),
        ('Professional Services (Direct)', 'Professional Services (Direct)'),
        ('Advertising', 'Advertising'),
        ('Traveling Expenses', 'Traveling Expenses'),
        ('Communication Expenses', 'Communication Expenses'),
        ('Internet Service Provider', 'Internet Service Provider'),
        ('Representation', 'Representation'),
        ('Other Profressinal Services', 'Other Professional Services'),
        ('Printing and Binding (Promotional)', 'Printing and Binding (Promotional)'),
        ('Professional Services (Indirect)', 'Professional Services (Indirect)'),
        ('Supplies and Materials', 'Supplies and Materials'),
        ('Utility', 'Utility'),
        ('Printing and Binding (Indirect)', 'Printing and Binding (Indirect)'),
        ('Maintenance', 'Maintenance'),
        ('Equipment Outlay', 'Equipment Outlay')
    )

    budget = models.ForeignKey(Budget)
    name = models.CharField(max_length=200, choices=ITEM_CHOICES,verbose_name="Line item")
    description = models.CharField(max_length=500, blank=True)
    amount = models.FloatField(default=0.0)

    def __str__(self):
        return self.get_name_display()


class Disbursement(models.Model):
    budget = models.ForeignKey(Budget)
    line_item = GF(LineItem, 
                   chained_field='budget', chained_model_field='budget',
                   on_delete=PROTECT)
    description = models.CharField(max_length=500, blank=True)
    amount = models.FloatField(default=0.0)


class BudgetRelease(models.Model):
    budget = models.ForeignKey(Budget)
    release_date = models.DateField(help_text='Format: YYYY-MM-DD')
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'DOST Fund Release'
        verbose_name_plural = 'DOST Fund Releases'

    def __str__(self):
        return '%s: %s' % (self.description, str(self.budget))

    def total_amount(self):
        total_amount = self.lineitembudgetrelease_set.aggregate(Sum('amount')).values()[0]
        if not total_amount:
            return '0.00'
        else:
            return '{:,.2f}'.format(total_amount)
        return total_amount if total_amount else '0.00'
    total_amount.short_description = 'Total amount'

class LineItemBudgetRelease(models.Model):
    budget_release = models.ForeignKey(BudgetRelease)
    line_item = models.ForeignKey(LineItem)
    description = models.CharField(max_length=500, blank=True)
    amount = models.FloatField(default=0.0)
