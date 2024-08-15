# Generated by Django 3.2.25 on 2024-08-10 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hostel_Admission', '0010_auto_20240811_0307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hosteldata1',
            name='shift',
        ),
        migrations.RemoveField(
            model_name='hosteldata2',
            name='shift',
        ),
        migrations.RemoveField(
            model_name='hosteldata3',
            name='shift',
        ),
        migrations.AlterField(
            model_name='hosteldata1',
            name='Branch',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='hosteldata1',
            name='cast',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='hosteldata2',
            name='Branch',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='hosteldata2',
            name='cast',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='hosteldata2',
            name='occupation',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='hosteldata3',
            name='Branch',
            field=models.CharField(max_length=40),
        ),
    ]