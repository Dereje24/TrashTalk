# Generated by Django 2.0.2 on 2018-03-20 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cleanups', '0013_auto_20180320_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requiredtools',
            name='tool_category',
        ),
        migrations.AddField(
            model_name='tool',
            name='tool_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cleanups.ToolCategory'),
        ),
    ]