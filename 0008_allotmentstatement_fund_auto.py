from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nia_app', '0007_allotmentstatement_ada_received_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='allotmentstatement',
            name='fund_type',
            field=models.CharField(
                blank=True, default='',
                choices=[('COB','501 COB'),('LFPs','501 LFPs'),('CARP','501 CARP'),('','Other')],
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name='allotmentstatement',
            name='province',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='allotmentstatement',
            name='cis_name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='allotmentstatement',
            name='source_advice',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='allotment_statements',
                to='nia_app.suballotmentadvice',
            ),
        ),
    ]
