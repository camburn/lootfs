from django.db import models

# Create your models here.

class Dungeon(models.Model):
    name = models.CharField(max_length=32)

class Boss(models.Model):
    name = models.CharField(max_length=32)
    dungeon = models.ForeignKey('Dungeon', on_delete=models.CASCADE)

class Item(models.Model):
    dropped_by = models.ForeignKey('Boss', on_delete=models.CASCADE)

class Raid(models.Model):
    dungeon = models.ForeignKey('Dungeon', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class PlayerClass(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=32)
    player_class = models.ForeignKey('PlayerClass', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    raid = models.ForeignKey('Raid', on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    consume_uptime = models.IntegerField()
    raid_parse_average = models.IntegerField()

class LootList(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    priority = models.IntegerField(unique=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
