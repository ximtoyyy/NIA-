from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nia_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllotmentStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=500, verbose_name='Name of Projects/Activities/Programs')),
                ('ada_number', models.CharField(max_length=100, verbose_name='ADA No.')),
                ('allotment_received', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Allotment Received (PHP)')),
                ('date', models.DateField(verbose_name='Date')),
                ('remarks', models.TextField(blank=True, verbose_name='Remarks')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Allotment Statement',
                'verbose_name_plural': 'Allotment Statements',
                'ordering': ['-date'],
            },
        ),
    ]
