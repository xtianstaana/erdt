from django.db import models
from django.db.models import Q, F, Sum, SET_NULL, PROTECT
from django.contrib.auth.models import User

# Create your models here.
class Token(models.Model):
    created_date = models.DateTimeField()
    code = models.CharField(max_length=100, unique=True)

class ApplicationPeriod(models.Model):
    name = models.CharField(max_length=250)
    created_date = models.DateTimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Application Period'
        verbose_name_plural = 'Application Periods'

class RecommendationForm(models.Model):
    NOT_STARTED, IN_PROGRESS, SUBMITTED = 'Not Started', 'In Progress', 'Submitted'
    STATUS_CHOICES = (
        (IN_PROGRESS, IN_PROGRESS),
        (SUBMITTED, SUBMITTED),
        (NOT_STARTED, NOT_STARTED)
    )

    application_period = models.ForeignKey(
        ApplicationPeriod, verbose_name='Application Period', null=True, blank=True, unique=False, on_delete=SET_NULL)

    # System Fields
    token = models.ForeignKey(Token)
    created_by = models.ForeignKey(
        User, verbose_name='Created by', null=True, blank=True, unique=False, on_delete=SET_NULL, related_name='recommendationforms_created')
    created_date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=100)
    sent_by = models.ForeignKey(
        User, verbose_name='Sent by', null=True, blank=True, unique=False, on_delete=SET_NULL, related_name='recommendationforms_sent')
    sent_date = models.DateTimeField()

    professor_email = models.EmailField()
    professor_name = models.CharField(max_length=250)

    # Form fields
    recommendation_box = models.CharField(verbose_name='Recommendation', max_length=500, blank=True)

class ERDTForm(models.Model):
    
    IN_PROGRESS, SUBMITTED = 'In Progress', 'Submitted'
    STATUS_CHOICES = (
        (IN_PROGRESS, IN_PROGRESS),
        (SUBMITTED, SUBMITTED),
    )

    ME_SCH, MS_SCH, DE_SCH, PHD_SCH = 'ME', 'MS', 'DE', 'PhD'
    SCHOLARSHIP_CHOICES = (
        (ME_SCH, ME_SCH),
        (MS_SCH, MS_SCH),
        (DE_SCH, DE_SCH),
        (PHD_SCH, PHD_SCH),
    )

    application_period = models.ForeignKey(
        ApplicationPeriod, verbose_name='Application Period', null=True, blank=True, unique=False, on_delete=SET_NULL)


    # System Fields
    created_by = models.ForeignKey(
        User, verbose_name='Created by', null=True, blank=True, unique=False, on_delete=SET_NULL)
    created_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=100)

    # Form Fields
    scholarship_applied_for = models.CharField(choices=SCHOLARSHIP_CHOICES, max_length=100)
    program_of_study = models.CharField(max_length=250)

