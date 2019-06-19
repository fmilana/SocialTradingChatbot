# Generated by Django 2.2.1 on 2019-06-18 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('next_task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='imagetagging.ImageTask')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=128)),
                ('correct', models.BooleanField(default=False)),
                ('image_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imagetagging.ImageTask')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('image_task', 'user', 'label')},
            },
        ),
    ]
