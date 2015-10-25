# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applicationforms', '0006_erdtform_last_modified_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='status',
            field=models.CharField(default='Not Started', max_length=100, choices=[(b'In Progress', b'In Progress'), (b'Submitted', b'Submitted'), (b'Not Started', b'Not Started')]),
            preserve_default=False,
        ),
    ]
