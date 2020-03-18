# Generated by Django 3.0.4 on 2020-03-13 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
