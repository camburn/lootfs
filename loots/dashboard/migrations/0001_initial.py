# Generated by Django 3.2.3 on 2021-05-29 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Boss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Dungeon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('wowhead_link', models.TextField()),
                ('icon_link', models.TextField()),
                ('dropped_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.boss')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerClass',
            fields=[
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Raid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_id', models.CharField(max_length=32)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('fights', models.IntegerField()),
                ('dungeon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.dungeon')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('alt', models.BooleanField(default=False)),
                ('main', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.player')),
                ('player_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.playerclass')),
            ],
        ),
        migrations.CreateModel(
            name='LootList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(unique=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.item')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.player')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.slot'),
        ),
        migrations.AddField(
            model_name='boss',
            name='dungeon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.dungeon'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('consume_uptime', models.IntegerField(default=0)),
                ('raid_parse_average', models.IntegerField(default=0)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.player')),
                ('raid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.raid')),
            ],
        ),
    ]
