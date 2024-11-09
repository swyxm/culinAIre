# Generated by Django 5.1.2 on 2024-10-29 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='flavorMetrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sweetness', models.FloatField(default=0.0)),
                ('saltiness', models.FloatField(default=0.0)),
                ('spiciness', models.FloatField(default=0.0)),
                ('sourness', models.FloatField(default=0.0)),
                ('bitterness', models.FloatField(default=0.0)),
                ('tanginess', models.FloatField(default=0.0)),
                ('richness', models.FloatField(default=0.0)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]
