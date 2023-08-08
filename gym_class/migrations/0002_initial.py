# Generated by Django 3.2.12 on 2022-11-29 06:33


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gym_student', '0001_initial'),
        ('gym_class', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='gym_student.student'),
        ),
        migrations.AddField(
            model_name='absentrequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='absent_requests', to='gym_student.student'),
        ),
    ]
