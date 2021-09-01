# Generated by Django 3.1.2 on 2021-08-29 07:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import score_list_app.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('score_list_app', '0003_auto_20210828_0807'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(upload_to='static/', validators=[score_list_app.validators.validate_file_extension])),
                ('created', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]