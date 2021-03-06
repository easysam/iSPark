# Generated by Django 2.2.1 on 2019-07-10 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BerthBelong',
            fields=[
                ('berth', models.CharField(max_length=6, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'berth_belong',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BlocksCapacity',
            fields=[
                ('block_id', models.AutoField(primary_key=True, serialize=False)),
                ('district', models.CharField(blank=True, max_length=3, null=True)),
                ('area', models.CharField(blank=True, max_length=10, null=True)),
                ('road', models.CharField(blank=True, max_length=12, null=True)),
                ('left_or_right', models.CharField(blank=True, max_length=2, null=True)),
                ('direction', models.CharField(blank=True, max_length=2, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=8, null=True)),
                ('type', models.CharField(blank=True, max_length=4, null=True)),
                ('strategy', models.CharField(blank=True, max_length=8, null=True)),
                ('capacity', models.BigIntegerField()),
            ],
            options={
                'db_table': 'blocks_capacity',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OccupancyList',
            fields=[
                ('record_id', models.AutoField(primary_key=True, serialize=False)),
                ('admin_region', models.CharField(blank=True, max_length=10, null=True)),
                ('berthage', models.CharField(blank=True, max_length=8, null=True)),
                ('in_time', models.DateTimeField(blank=True, null=True)),
                ('out_time', models.DateTimeField(blank=True, null=True)),
                ('section', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'occupancy_list',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RoadList',
            fields=[
                ('road', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('longitude', models.CharField(blank=True, max_length=18, null=True)),
                ('latitude', models.CharField(blank=True, max_length=18, null=True)),
                ('area', models.CharField(blank=True, max_length=3, null=True)),
                ('capacity', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'road_list',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RoadShape',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('road', models.CharField(max_length=12)),
                ('shape', models.TextField()),
            ],
        ),
    ]
