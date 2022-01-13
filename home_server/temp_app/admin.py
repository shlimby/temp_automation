from django.contrib import admin

# Register your models here. => Models here can be modifierd by admin
from .models import ChatUser, Sensor, Entrie, Room, Place, OutsideEntrie

admin.site.register(ChatUser)
admin.site.register(Sensor)
admin.site.register(Entrie)
admin.site.register(Room)
admin.site.register(Place)
admin.site.register(OutsideEntrie)
