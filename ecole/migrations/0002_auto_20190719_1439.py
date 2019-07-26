# Generated by Django 2.2.3 on 2019-07-19 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecole', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
                ('school_name', models.CharField(max_length=100)),
                ('school_address', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=100),
        ),
    ]
