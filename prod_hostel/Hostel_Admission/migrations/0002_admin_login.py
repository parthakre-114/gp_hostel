# Generated by Django 5.0.7 on 2024-08-05 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hostel_Admission', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_login',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.IntegerField()),
                ('passwd', models.CharField(max_length=255)),
            ],
        ),
    ]
