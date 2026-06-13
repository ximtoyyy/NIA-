from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubAllotmentAdvice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advice_number', models.CharField(max_length=100, unique=True)),
                ('date', models.DateField()),
                ('calendar_year', models.IntegerField()),
                ('region', models.CharField(choices=[('1', 'Region 1 - Ilocos Region'), ('2', 'Region 2 - Cagayan Valley'), ('3', 'Region 3 - Central Luzon'), ('4A', 'Region 4A - CALABARZON'), ('4B', 'Region 4B - MIMAROPA'), ('5', 'Region 5 - Bicol Region'), ('6', 'Region 6 - Western Visayas'), ('7', 'Region 7 - Central Visayas'), ('8', 'Region 8 - Eastern Visayas'), ('9', 'Region 9 - Zamboanga Peninsula'), ('10', 'Region 10 - Northern Mindanao'), ('11', 'Region 11 - Davao Region'), ('12', 'Region 12 - SOCCSKSARGEN'), ('13', 'Region 13 - Caraga'), ('CAR', 'CAR - Cordillera Administrative Region'), ('NCR', 'NCR - National Capital Region'), ('BARMM', 'BARMM - Bangsamoro')], max_length=10)),
                ('to_office', models.CharField(default='REGIONAL IRRIGATION MANAGER', max_length=200)),
                ('to_location', models.CharField(max_length=200)),
                ('fund_code', models.CharField(blank=True, max_length=20)),
                ('gaa_saro_number', models.CharField(blank=True, max_length=100)),
                ('object_code', models.CharField(blank=True, max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('amount_in_words', models.CharField(blank=True, max_length=500)),
                ('certified_by_name', models.CharField(blank=True, max_length=200)),
                ('certified_by_title', models.CharField(blank=True, max_length=200)),
                ('recommended_by_name', models.CharField(blank=True, max_length=200)),
                ('recommended_by_title', models.CharField(blank=True, max_length=200)),
                ('approved_by_name', models.CharField(blank=True, max_length=200)),
                ('approved_by_title', models.CharField(blank=True, max_length=200)),
                ('ada_number', models.CharField(blank=True, max_length=100, null=True)),
                ('ada_date', models.DateField(blank=True, null=True)),
                ('ada_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Sub-Allotment Advice',
                'verbose_name_plural': 'Sub-Allotment Advices',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='ProvinceAllotment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province_name', models.CharField(max_length=200)),
                ('province_total', models.DecimalField(decimal_places=2, max_digits=15)),
                ('order', models.PositiveIntegerField(default=0)),
                ('sub_allotment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='province_allotments', to='nia_app.suballotmentadvice')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='CISAllotment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cis_name', models.CharField(max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('order', models.PositiveIntegerField(default=0)),
                ('province_allotment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cis_allotments', to='nia_app.provinceallotment')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
