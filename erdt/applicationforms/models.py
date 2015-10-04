from django.db import models
from django.db.models import Q, F, Sum, SET_NULL, PROTECT
from django.contrib.auth.models import User

# Create your models here.
class Token(models.Model):
    created_date = models.DateTimeField()
    code = models.CharField(max_length=100, unique=True)

class RecommendationForm(models.Model):
    IN_PROGRESS, SUBMITTED = 'In Progress', 'Submitted'
    STATUS_CHOICES = (
        (IN_PROGRESS, IN_PROGRESS),
        (SUBMITTED, SUBMITTED),
    )

    # System Fields
    token = models.ForeignKey(Token)
    created_by = models.ForeignKey(
        User, verbose_name='Created by', null=True, blank=True, unique=True, on_delete=SET_NULL)
    created_date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=100)

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

    # System Fields
    created_by = models.ForeignKey(
        User, verbose_name='Created by', null=True, blank=True, unique=True, on_delete=SET_NULL)
    created_date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=100)

    # Form Fields
    scholarship_applied_for = models.CharField(choices=SCHOLARSHIP_CHOICES, max_length=100)
    program_of_study = models.CharField(max_length=250)


class Recommendation(models.Model):
    erdt_form = models.ForeignKey(ERDTForm)

    professor_email = models.EmailField()
    recommendation_form = models.ForeignKey(RecommendationForm)

