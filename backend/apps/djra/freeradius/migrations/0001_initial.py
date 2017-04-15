# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Radacct',
            fields=[
                ('radacctid', models.AutoField(serialize=False, primary_key=True)),
                ('acctsessionid', models.CharField(max_length=32)),
                ('acctuniqueid', models.CharField(max_length=32)),
                ('username', models.CharField(max_length=253, null=True)),
                ('groupname', models.CharField(max_length=253, null=True)),
                ('realm', models.CharField(max_length=64, null=True)),
                ('nasipaddress', models.GenericIPAddressField()),
                ('nasportid', models.CharField(max_length=15, null=True)),
                ('nasporttype', models.CharField(max_length=32, null=True)),
                ('acctstarttime', models.DateTimeField(null=True)),
                ('acctstoptime', models.DateTimeField(null=True)),
                ('acctsessiontime', models.BigIntegerField(null=True)),
                ('acctauthentic', models.CharField(max_length=32, null=True)),
                ('acctinputoctets', models.BigIntegerField(null=True)),
                ('acctoutputoctets', models.BigIntegerField(null=True)),
                ('calledstationid', models.CharField(max_length=50, null=True)),
                ('callingstationid', models.CharField(max_length=50, null=True)),
                ('framedipaddress', models.GenericIPAddressField(null=True)),
                ('connectinfo_start', models.CharField(max_length=50, null=True)),
                ('connectinfo_stop', models.CharField(max_length=50, null=True)),
                ('acctterminatecause', models.CharField(max_length=32, null=True)),
                ('servicetype', models.CharField(max_length=32, null=True)),
                ('framedprotocol', models.CharField(max_length=32, null=True)),
                ('acctstartdelay', models.IntegerField(null=True)),
                ('acctstopdelay', models.IntegerField(null=True)),
                ('xascendsessionsvrkey', models.CharField(max_length=10, null=True)),
            ],
            options={
                'db_table': 'radacct',
                'verbose_name_plural': 'radacct',
            },
        ),
        migrations.CreateModel(
            name='Radcheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64)),
                ('attribute', models.CharField(max_length=64)),
                ('op', models.CharField(max_length=2, choices=[(b'=', b'='), (b':=', b':='), (b'==', b'=='), (b'+=', b'+='), (b'!=', b'!='), (b'>', b'>'), (b'>=', b'>='), (b'<', b'<'), (b'<=', b'<='), (b'=~', b'=~'), (b'!~', b'!~'), (b'=*', b'=*'), (b'!*', b'!*')])),
                ('value', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'radcheck',
                'verbose_name_plural': 'radcheck',
            },
        ),
        migrations.CreateModel(
            name='Radgroupcheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('groupname', models.CharField(max_length=64)),
                ('attribute', models.CharField(max_length=64)),
                ('op', models.CharField(max_length=2, choices=[(b'=', b'='), (b':=', b':='), (b'==', b'=='), (b'+=', b'+='), (b'!=', b'!='), (b'>', b'>'), (b'>=', b'>='), (b'<', b'<'), (b'<=', b'<='), (b'=~', b'=~'), (b'!~', b'!~'), (b'=*', b'=*'), (b'!*', b'!*')])),
                ('value', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'radgroupcheck',
                'verbose_name_plural': 'radgroupcheck',
            },
        ),
        migrations.CreateModel(
            name='Radgroupreply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('groupname', models.CharField(max_length=64)),
                ('attribute', models.CharField(max_length=64)),
                ('op', models.CharField(max_length=2, choices=[(b'=', b'='), (b':=', b':='), (b'+=', b'+=')])),
                ('value', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'radgroupreply',
                'verbose_name_plural': 'radgroupreply',
            },
        ),
        migrations.CreateModel(
            name='Radippool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pool_name', models.CharField(help_text=b'The IP Pool name', max_length=64)),
                ('framedipaddress', models.GenericIPAddressField(help_text=b'The users IP address')),
                ('nasipaddress', models.CharField(max_length=16)),
                ('callingstationid', models.TextField(help_text=b'The MAC Address or CLI of the user', verbose_name=b'Calling-Station-Id')),
                ('expiry_time', models.DateTimeField(help_text=b'The IP Lease expiry time')),
                ('username', models.CharField(max_length=64)),
                ('groupname', models.CharField(max_length=30)),
                ('pool_key', models.CharField(max_length=30)),
                ('fixed', models.BooleanField()),
            ],
            options={
                'db_table': 'radippool',
                'verbose_name_plural': 'radippool',
            },
        ),
        migrations.CreateModel(
            name='Radpostauth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64, db_column=b'pass')),
                ('reply', models.CharField(max_length=32)),
                ('authdate', models.DateTimeField()),
                ('calledstationid', models.CharField(max_length=64)),
                ('callingstationid', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'radpostauth',
                'verbose_name_plural': 'radpostauth',
            },
        ),
        migrations.CreateModel(
            name='Radreply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=30)),
                ('attribute', models.CharField(max_length=30)),
                ('op', models.CharField(max_length=2, choices=[(b'=', b'='), (b':=', b':='), (b'+=', b'+=')])),
                ('value', models.CharField(max_length=40)),
                ('calledstationid', models.CharField(max_length=64)),
                ('custid', models.IntegerField()),
            ],
            options={
                'db_table': 'radreply',
                'verbose_name_plural': 'radreply',
            },
        ),
        migrations.CreateModel(
            name='Radusergroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=30)),
                ('groupname', models.CharField(max_length=30)),
                ('priority', models.IntegerField()),
            ],
            options={
                'db_table': 'radusergroup',
            },
        ),
        migrations.CreateModel(
            name='RadUser',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('freeradius.radcheck',),
        ),
    ]
