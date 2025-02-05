# Generated by Django 3.1.1 on 2021-03-21 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barangay', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('admin', models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('datePromoted', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=45, null=True)),
                ('type', models.CharField(blank=True, max_length=45, null=True)),
                ('description', models.CharField(max_length=100)),
                ('datetime_start', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('datetime_end', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('upvotes', models.IntegerField(blank=True, default=0, null=True)),
                ('participants', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestType', models.CharField(choices=[('Join Event', 'Join Event'), ('Promote to Organizer', 'Promote to Organizer'), ('Promote to Admin', 'Promote to Admin')], default='Join Event', max_length=30, null=True)),
                ('status', models.CharField(choices=[('For Review', 'For Review'), ('Accepted', 'Accepted'), ('Denied', 'Denied')], default='For Review', max_length=30, null=True)),
                ('datetime_request', models.DateTimeField(auto_now_add=True)),
                ('datetime_reply', models.DateTimeField(blank=True, null=True)),
                ('replied_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('organizer', models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('datePromoted', models.DateField(auto_now_add=True)),
                ('event', models.ManyToManyField(blank=True, to='app.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=100)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.request')),
            ],
        ),
    ]
