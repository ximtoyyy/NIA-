from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nia_app', '0003_update_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='GAASAROMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=300, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name': 'GAA/SARO Master', 'ordering': ['value']},
        ),
        migrations.CreateModel(
            name='ObjectCodeMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name': 'Object Code Master', 'ordering': ['value']},
        ),
        migrations.CreateModel(
            name='DescriptionMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=500, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name': 'Description Master', 'ordering': ['value']},
        ),
        migrations.CreateModel(
            name='AdviceNumberMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name': 'Advice Number Master', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='CISMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=200)),
                ('cis_name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name': 'CIS Master', 'ordering': ['province', 'cis_name']},
        ),
        migrations.AlterUniqueTogether(
            name='cismaster',
            unique_together={('province', 'cis_name')},
        ),
    ]
