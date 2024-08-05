# Generated by Django 5.0.7 on 2024-07-28 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0004_rename_meal_type_meal_meal_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='member_email',
        ),
        migrations.AddField(
            model_name='meal',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='foodimage',
            name='member_email',
            field=models.EmailField(max_length=254),
        ),
    ]
