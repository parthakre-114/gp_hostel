# Generated by Django 5.0.7 on 2024-08-07 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hostel_Admission', '0003_alter_admin_login_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('categories', models.CharField(max_length=255)),
            ],
        ),
    ]