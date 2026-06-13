from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nia_app', '0002_allotmentstatement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suballotmentadvice',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='suballotmentadvice',
            name='to_location',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='suballotmentadvice',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='suballotmentadvice',
            name='description',
            field=models.CharField(blank=True, default='Repair of Communal Irrigation Systems', max_length=500),
        ),
        migrations.AlterField(
            model_name='suballotmentadvice',
            name='gaa_saro_number',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
