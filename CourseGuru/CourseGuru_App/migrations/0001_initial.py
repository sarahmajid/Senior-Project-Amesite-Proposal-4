# Generated by Django 2.0.1 on 2018-01-28 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('answer', models.CharField(max_length=400)),
                ('comments', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseName', models.CharField(max_length=50)),
                ('courseType', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('question', models.CharField(max_length=200)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CourseGuru_App.course')),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=30)),
                ('lastName', models.CharField(max_length=50)),
                ('userId', models.CharField(max_length=8)),
                ('status', models.CharField(max_length=18)),
            ],
        ),
        migrations.AddField(
            model_name='questions',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CourseGuru_App.user'),
        ),
        migrations.AddField(
            model_name='course',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CourseGuru_App.user'),
        ),
        migrations.AddField(
            model_name='answers',
            name='question_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CourseGuru_App.questions'),
        ),
        migrations.AddField(
            model_name='answers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CourseGuru_App.user'),
        ),
    ]
