# Generated by Django 4.2.5 on 2023-09-19 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('release_date', models.DateField()),
                ('rating_average', models.DecimalField(decimal_places=1, max_digits=3)),
                ('vote_count', models.IntegerField()),
            ],
        ),
    ]
