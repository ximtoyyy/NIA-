from django.db import migrations


def seed_data(apps, schema_editor):
    GAASAROMaster = apps.get_model('nia_app', 'GAASAROMaster')
    ObjectCodeMaster = apps.get_model('nia_app', 'ObjectCodeMaster')
    DescriptionMaster = apps.get_model('nia_app', 'DescriptionMaster')
    CISMaster = apps.get_model('nia_app', 'CISMaster')

    # GAA/SARO
    for v in [
        'NBC No. 595, RA No. 12116\nFY 2025 GAA',
        'NBC No. 596, RA No. 12117\nFY 2026 GAA',
    ]:
        GAASAROMaster.objects.get_or_create(value=v)

    # Object Codes
    for v in ['1-06-10-020', '1-06-10-030', '1-06-10-040']:
        ObjectCodeMaster.objects.get_or_create(value=v)

    # Descriptions
    for v in [
        'Repair of Communal Irrigation Systems',
        'Construction of Communal Irrigation Systems',
        'Rehabilitation of Communal Irrigation Systems',
        'Construction of Irrigation Facilities',
        'Rehabilitation of Irrigation Systems',
        'Maintenance and Repair Works',
        'Improvement of Communal Irrigation Systems',
    ]:
        DescriptionMaster.objects.get_or_create(value=v)

    # CIS Master Data
    caraga_cis = {
        'AGUSAN DEL NORTE': ['Santiago CIS','Caimpugan CIS','Jabonga CIS','Kitcharao CIS','Las Nieves CIS','Magallanes CIS','Nasipit CIS','Remedios T. Romualdez CIS','Tubay CIS','Carmen CIS'],
        'AGUSAN DEL SUR': ['Bayugan CIS','Bunawan CIS','Esperanza CIS','La Paz CIS','Loreto CIS','Prosperidad CIS','Rosario CIS','San Francisco CIS','San Luis CIS','Santa Josefa CIS','Sibagat CIS','Talacogon CIS','Trento CIS','Veruela CIS'],
        'DINAGAT ISLANDS': ['Basilisa CIS','Cagdianao CIS','Dinagat CIS','Doña Helene CIS','Ferdinand CIS','Libjo CIS','Loreto CIS','San Jose CIS','Villa Ecleo CIS'],
        'SURIGAO DEL NORTE': ['Alegria CIS','Bacuag CIS','Burgos CIS','Claver CIS','Dapa CIS','Del Carmen CIS','Esperanza CIS','General Luna CIS','Gigaquit CIS','Mainit CIS','Malimono CIS','Pilar CIS','Placer CIS','San Benito CIS','San Francisco CIS','San Isidro CIS','Santa Monica CIS','Sison CIS','Socorro CIS','Surigao City CIS','Tagana-an CIS','Tubod CIS','Sayak CIS','San Pedro CIS','San Roque CIS'],
        'SURIGAO DEL SUR': ['Barobo CIS','Bayabas CIS','Bislig City CIS','Cagwait CIS','Cantilan CIS','Carmen CIS','Carrascal CIS','Cortes CIS','Hinatuan CIS','Lanuza CIS','Lianga CIS','Lingig CIS','Madrid CIS','Marihatag CIS','San Agustin CIS','San Miguel CIS','Tagbina CIS','Tago CIS','Tandag City CIS','Tidman CIS'],
    }
    for province, cis_list in caraga_cis.items():
        for cis in cis_list:
            CISMaster.objects.get_or_create(province=province, cis_name=cis)


class Migration(migrations.Migration):
    dependencies = [
        ('nia_app', '0004_master_tables'),
    ]
    operations = [
        migrations.RunPython(seed_data, migrations.RunPython.noop),
    ]
