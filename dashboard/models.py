from django.db import models

# Create your models here.

class Dungeon(models.Model):
    name = models.CharField()

class Boss(models.Model):
    name = models.CharField()
    dungeon = models.ForeignKey('Dungeon')

class Item(models.Model):
    dropped_by = models.ForeignKey('Boss')

class Raid(models.Model):
    dungeon = models.ForeignKey('Dungeon')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Class(models.Model):
    name = models.CharField()

class Player(models.Model):
    name = models.CharField()
    player_class = models.ForeignKey('Class')

class Attendance(models.Model):
    raid = models.ForeignKey('Raid')
    player = models.ForeignKey('Player')
    consume_uptime = models.IntegerField()
    raid_parse_average = models.IntegerField()

class LootList(models.Model):
    player = models.ForeignKey('Player')
    priority = models.IntegerField(unique=True)
    item = models.ForeignKey('Item')
