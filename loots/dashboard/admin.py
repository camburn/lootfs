from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Player, PlayerClass, Dungeon, Raid, Attendance, Item, Slot, Boss

admin.site.register(Player)
admin.site.register(PlayerClass)
admin.site.register(Dungeon)
admin.site.register(Raid)
admin.site.register(Attendance)
admin.site.register(Item)
admin.site.register(Slot)
admin.site.register(Boss)
