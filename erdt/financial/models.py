from django.db import models
from django.db.models import PROTECT, Sum
from polymorphic import PolymorphicModel
from datetime import datetime, date
from smart_selects.db_fields import ChainedForeignKey as GF
from profiling import models as profiling_models
from django.core.exceptions import ValidationError
from django.utils.html import format_html, mark_safe


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
        out = u'<table class="table table-bordered table-condensed table-striped"><thread><tr> <td><b>Line Item</b></td> <td><b>Budget</b></td>' \
            '<td><b>Released</b></td> <td><b>Unexpended</b></td></tr>'

        _temp =  '<td> %s </td>' + ('<td class="numeric"> %s </td> ' * 3)

        f_budget, f_released, f_unxpended = self.summary_local_common('Scholarship (Local): Tuition and Fees', 'TUITION')

        out += '<tr> %s </tr>' % (_temp % ('Tuition and Fees', '{:,.2f}'.format(f_budget), 
            '{:,.2f}'.format(f_released), '{:,.2f}'.format(f_unxpended)))


        f_budget, f_released, f_unxpended = self.summary_local_common('Scholarship (Local): Stipends', 'STIPEND')

        out += '<tr> %s </tr>' % (_temp % ('Stipends', '{:,.2f}'.format(f_budget), 
            '{:,.2f}'.format(f_released), '{:,.2f}'.format(f_unxpended)))

        f_budget, f_released, f_unxpended = self.summary_local_common('Scholarship (Local): Book Allowance', 'BOOK_ALW')

        out += '<tr> %s </tr>' % (_temp % ('Book Allowance', '{:,.2f}'.format(f_budget), 
            '{:,.2f}'.format(f_released), '{:,.2f}'.format(f_unxpended)))

        out += '</thread></table>'

        return format_html(mark_safe(out))
    release_scholarship_local.short_description = 'Scholarship (Local)'

    def release_sandwich(self):
        out = u'<table class="table table-bordered table-condensed table-striped"><thread><tr> <td><b>Line Item</b></td> <td><b>Budget</b></td>' \
            '<td><b>Released</b></td> <td><b>Unexpended</b></td></tr>'
        _temp =  '<td> %s </td>' + ('<td class="numeric"> %s </td> ' * 3)

        f_budget, f_released, f_unxpended = self.summary_sandwich()

        out += '<tr> %s </tr>' % (_temp % ('Sandwich', '{:,.2f}'.format(f_budget), 
            '{:,.2f}'.format(f_released), '{:,.2f}'.format(f_unxpended)))
        out += '</thread></table>'
        print 'xxx',out,'xxx'
        return format_html(mark_safe(out))
    release_sandwich.short_description = 'Sandwich Program'

    def summary_sandwich(self):
        allocation = self.lineitem_set.filter(name='Sandwich Program')
        if allocation:
            total_allocation = allocation[0].ammount
        else:
            total_allocation = 0.0

        released = profiling_models.Sandwich_Program.objects.filter(start_date__gt=self.start_date, 
            end_date__lt=self.end_date)

        total_released = 0.0

        for release in released:
                total_released += release.total_released()

        total_released = 0.0
        total_unexpended = total_allocation - total_released

        return total_allocation, total_released, total_unexpended


    def summary_local_common(self, name, alloc_name):
        allocation = self.lineitem_set.filter(name=name)
        if allocation:
            total_allocation = allocation[0].ammount
        else:
            total_allocation = 0.0

        released = profiling_models.Grant_Allocation_Release.objects.filter(date_released__gte=self.start_date, 
            date_released__lte=self.end_date, allocation__name=alloc_name)

        total_released = 0.0

        for release in released:
            if isinstance(release.grant, profiling_models.Scholarship):
                total_released += release.amount_released

        total_unexpended = total_allocation - total_released

        return total_allocation, total_released, total_unexpended

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
    release_date = models.DateField(help_text='Format: YYYY-MM-DD')
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
