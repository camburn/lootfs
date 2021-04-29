from django.db import models
from django_pandas.managers import DataFrameManager

# Create your models here.

class Dungeon(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Boss(models.Model):
    name = models.CharField(max_length=32)
    dungeon = models.ForeignKey('Dungeon', on_delete=models.CASCADE)

class Slot(models.Model):
    name = models.CharField(max_length=255)

class Item(models.Model):
    name = models.CharField(max_length=255)
    slot = models.ForeignKey('Slot', on_delete=models.CASCADE)
    dropped_by = models.ForeignKey('Boss', on_delete=models.CASCADE)
    wowhead_link = models.TextField()
    icon_link = models.TextField()

    def __str__(self):
        return f'{self.name}'

class Raid(models.Model):
    dungeon = models.ForeignKey('Dungeon', on_delete=models.CASCADE)
    report_id = models.CharField(max_length=32)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    fights = models.IntegerField()

    @property
    def name(self):
        return self.__str__()

    def __str__(self):
        return f'{self.dungeon.name} - {self.start_time.date()}'

class PlayerClass(models.Model):
    name = models.CharField(max_length=32, primary_key=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=32, unique=True)
    player_class = models.ForeignKey('PlayerClass', on_delete=models.CASCADE)
    alt = models.BooleanField(default=False)
    main = models.ForeignKey('Player', on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    raid = models.ForeignKey('Raid', on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    consume_uptime = models.IntegerField(default=0)
    raid_parse_average = models.IntegerField(default=0)

class LootList(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    priority = models.IntegerField(unique=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
