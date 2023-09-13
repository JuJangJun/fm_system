# Generated by Django 4.2.4 on 2023-08-16 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Attendance",
            fields=[
                ("att_id", models.AutoField(primary_key=True, serialize=False)),
                ("w_id", models.PositiveIntegerField()),
                ("attend_time", models.DateTimeField(auto_now_add=True)),
                ("leave_time", models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Safety_check",
            fields=[
                ("sc_id", models.AutoField(primary_key=True, serialize=False)),
                ("sc_code", models.CharField(max_length=20)),
                ("att_id", models.PositiveIntegerField()),
                ("w_id", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Workers",
            fields=[
                (
                    "w_id",
                    models.PositiveIntegerField(primary_key=True, serialize=False),
                ),
                ("wname", models.CharField(max_length=128)),
                ("manager_id", models.PositiveIntegerField(null=True)),
                ("contact", models.CharField(max_length=20)),
                ("email", models.EmailField(max_length=254, null=True)),
            ],
        ),
    ]