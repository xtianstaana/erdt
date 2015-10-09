# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applicationforms', '0003_recommendationform'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('erdt_form', models.ForeignKey(to='applicationforms.ERDTForm', to_field='id')),
                ('professor_email', models.EmailField(max_length=75)),
                ('recommendation_form', models.ForeignKey(to='applicationforms.RecommendationForm', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
