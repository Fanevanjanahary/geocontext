# Generated by Django 3.1 on 2020-08-18 07:38

import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(help_text='Key of collection.', max_length=200, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_key', message='Key must only contains lower case or underscore.', regex='^[0-9a-z_]+$')])),
                ('name', models.CharField(help_text='Display Name of Collection.', max_length=200)),
                ('description', models.TextField(blank=True, help_text='Description of the Collection.', null=True)),
            ],
            options={
                'ordering': ['key'],
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(help_text='Key of group.', max_length=200, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_key', message='Key must only contains lower case or underscore.', regex='^[0-9a-z_]+$')])),
                ('name', models.CharField(help_text='Display Name of Service.', max_length=200)),
                ('description', models.TextField(blank=True, help_text='Description of the Group.', null=True)),
                ('group_type', models.CharField(choices=[('text', 'Text'), ('graph', 'Graph')], default='text', help_text='Type of the group to determine the UI.', max_length=10)),
                ('permission_groups', models.ManyToManyField(blank=True, help_text='List of auth groups with access to this group.', to='auth.Group')),
            ],
            options={
                'ordering': ['key'],
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registry', models.CharField(help_text='Registry that was queried', max_length=200)),
                ('key', models.CharField(help_text='Query key', max_length=200)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(help_text='Queried point.', srid=4326)),
                ('tolerance', models.FloatField(blank=True, help_text='Query tolerance.', null=True)),
                ('output_format', models.CharField(help_text='Format requested', max_length=200)),
                ('created_time', models.DateTimeField(editable=False, help_text='Date of query.')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(help_text='Key of Service.', max_length=200, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_key', message='Key must only contains lower case or underscore.', regex='^[0-9a-z_]+$')])),
                ('name', models.CharField(help_text='Name of Service.', max_length=200)),
                ('description', models.CharField(blank=True, help_text='Description of Service.', max_length=1000, null=True)),
                ('url', models.CharField(help_text='URL of Service.', max_length=1000)),
                ('username', models.CharField(blank=True, help_text='User name for accessing Service.', max_length=200, null=True)),
                ('password', models.CharField(blank=True, help_text='Password for accessing Service.', max_length=200, null=True)),
                ('api_key', models.CharField(blank=True, help_text='API key for accessing Service.', max_length=200, null=True)),
                ('query_url', models.CharField(blank=True, help_text='Query URL for accessing Service.', max_length=1000, null=True)),
                ('query_type', models.CharField(choices=[('WFS', 'WFS'), ('WCS', 'WCS'), ('WMS', 'WMS'), ('REST', 'REST'), ('ArcREST', 'ArcREST'), ('Wikipedia', 'Wikipedia'), ('PlaceName', 'PlaceName')], help_text='Query type of the Service.', max_length=200)),
                ('layer_name', models.CharField(help_text='Required name of the actual layer/feature to retrieve (Property name.', max_length=200)),
                ('layer_namespace', models.CharField(blank=True, help_text='Optional namespace containing the typename to query (WMS/WFS).', max_length=200, null=True)),
                ('layer_typename', models.CharField(blank=True, help_text='Optional layer type name to get from the service (WMS/WFS).', max_length=200, null=True)),
                ('layer_workspace', models.CharField(blank=True, help_text='Optional workspace containing the typename to query (WMS/WFS).', max_length=200, null=True)),
                ('cache_duration', models.IntegerField(blank=True, default=604800, help_text='Service refresh time in seconds - determines Cache persistence', null=True)),
                ('srid', models.IntegerField(blank=True, default=4326, help_text='The Spatial Reference ID of the service.', null=True)),
                ('tolerance', models.FloatField(blank=True, default=10, help_text='Tolerance around query point in meters. Used for bounding box queries.Also determines cache hit range for all values', null=True)),
                ('service_version', models.CharField(help_text='Version of the service (e.g. WMS 1.1.0, WFS 2.0.0).', max_length=200)),
                ('provenance', models.CharField(blank=True, help_text='The origin or source of the Service.', max_length=1000, null=True)),
                ('notes', models.TextField(blank=True, help_text='Notes for the Service.', null=True)),
                ('licensing', models.CharField(blank=True, help_text='The licensing scheme for the Service.', max_length=1000, null=True)),
                ('test_x', models.FloatField(blank=True, help_text='Longitude of known value to test service.', null=True)),
                ('test_y', models.FloatField(blank=True, help_text='Latitude of known value to test service.', null=True)),
                ('test_value', models.CharField(blank=True, help_text='Known value expected at test coordinates.', max_length=1000, null=True)),
                ('status', models.BooleanField(blank=True, help_text='Status of this service (determined by test coordinate & value', null=True)),
                ('permission_groups', models.ManyToManyField(blank=True, help_text='List of auth groups with access to this service.', to='auth.Group')),
            ],
            options={
                'ordering': ['key'],
            },
        ),
        migrations.CreateModel(
            name='GroupServices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(blank=True, default=0, verbose_name='Order')),
                ('group', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='geocontext.group')),
                ('service', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='geocontext.service')),
            ],
            options={
                'unique_together': {('group', 'service')},
            },
        ),
        migrations.AddField(
            model_name='group',
            name='services',
            field=models.ManyToManyField(blank=True, help_text='List of services in the group.', through='geocontext.GroupServices', to='geocontext.Service'),
        ),
        migrations.CreateModel(
            name='CollectionGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(blank=True, default=0, verbose_name='Order')),
                ('collection', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='geocontext.collection')),
                ('group', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='geocontext.group')),
            ],
            options={
                'unique_together': {('collection', 'group')},
            },
        ),
        migrations.AddField(
            model_name='collection',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='List of group in this collection.', through='geocontext.CollectionGroups', to='geocontext.Group'),
        ),
        migrations.AddField(
            model_name='collection',
            name='permission_groups',
            field=models.ManyToManyField(blank=True, help_text='List of auth groups with access to this collection.', to='auth.Group'),
        ),
        migrations.CreateModel(
            name='Cache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of Cache.', max_length=200)),
                ('source_uri', models.CharField(blank=True, help_text='Source URI.', max_length=1000, null=True)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(blank=True, help_text='Geometry associated with the value (2d, EPSG:3857).', null=True, srid=3857)),
                ('value', models.CharField(blank=True, help_text='The value of the service.', max_length=200, null=True)),
                ('created_time', models.DateTimeField(editable=False, help_text='Date of cache entry.')),
                ('expired_time', models.DateTimeField(help_text='Date when the cache expires.')),
                ('service', models.ForeignKey(help_text='Service associated with the value.', on_delete=django.db.models.deletion.CASCADE, to='geocontext.service')),
            ],
        ),
    ]
