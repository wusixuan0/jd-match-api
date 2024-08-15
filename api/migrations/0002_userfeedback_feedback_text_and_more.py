# Generated by Django 5.0.7 on 2024-08-15 17:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfeedback',
            name='feedback_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='temporary_transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.temporarytransaction'),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='user_email',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.useremail'),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='user_ranking',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddConstraint(
            model_name='userfeedback',
            constraint=models.CheckConstraint(check=models.Q(('temporary_transaction__isnull', False), ('user_email__isnull', False), _connector='OR'), name='feedback_has_temporary_transaction_or_user'),
        ),
    ]
