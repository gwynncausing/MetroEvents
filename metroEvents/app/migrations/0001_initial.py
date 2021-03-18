# Generated by Django 3.1.1 on 2021-03-17 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField()),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('birthdate', models.DateField()),
                ('address', models.CharField(max_length=50)),
                ('userType', models.CharField(max_length=50)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.user')),
            ],
        ),
    ]
