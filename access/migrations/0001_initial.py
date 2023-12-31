# Generated by Django 4.2.4 on 2023-08-16 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Access",
            fields=[
                ("a_id", models.AutoField(primary_key=True, serialize=False)),
                ("w_id", models.PositiveIntegerField()),
                ("p_id", models.CharField(max_length=10)),
                ("in_time", models.DateTimeField(auto_now_add=True)),
                ("out_time", models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Place",
            fields=[
                (
                    "p_id",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                ("task_location", models.CharField(max_length=50)),
                ("danger_degree", models.PositiveIntegerField()),
                ("p_num", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Slack",
            fields=[
                ("slack_id", models.AutoField(primary_key=True, serialize=False)),
                ("msg", models.CharField(max_length=100, null=True)),
                ("p_id", models.CharField(max_length=10)),
                ("slack_time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
