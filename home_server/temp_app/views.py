from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from temp_app.common import get_settings, set_settings
from .models import Entrie, ChatUser, Room, Sensor, Place, OutsideEntrie
import json
from django.core import serializers

# Views on Homepage


def index(request):
    """Index View"""
    obj = serializers.serialize('json', Entrie.objects.all())
    obj_json = json.dumps(obj)
    outObj = serializers.serialize('json', OutsideEntrie.objects.all())
    outObj_json = json.dumps(outObj)
    sensObj = serializers.serialize('json', Sensor.objects.all())
    sensObj_json = json.dumps(sensObj)

    return render(request, 'temp_app/index.html', {'data': obj_json, 'sensors': sensObj_json, 'outData': outObj_json})


def settings(request):
    """View for Satting page"""

    # Get ChatUser, places and rooms
    chatusers = ChatUser.objects.all()
    places = Place.objects.all()
    rooms = Room.objects.all()

    # Get entries without sensors
    missing_entries = Entrie.objects.filter(sensor=None)

    single_ips = []

    # filter Setting by ID
    for entrie in missing_entries:
        is_in_array = False
        for sing_entrie in single_ips:
            if sing_entrie.ip == entrie.ip:
                is_in_array = True
                break
        if not is_in_array:
            single_ips.append(entrie)

    # Safe data in dict to use them in settings.html
    context = {
        "missing_entries": single_ips,
        "rooms": rooms,
        "chat_users": chatusers,
        "places": places,
        "room_type_choices": Room.room_type_choices,
        "settings": get_settings(),
    }
    return render(request, 'temp_app/settings.html', context)


def init_sensor(request):
    # Get Data for template
    sensors = Sensor.objects.order_by('-name')
    chat_user = ChatUser.objects.order_by('-username')
    rooms = Room.objects.order_by('-name')

    # Safe data in dict to use them in settings.html
    context = {
        "sensors": sensors,
        "place_options": Room.room_type_choices,
        # "chat_users": chat_user,
        "rooms": rooms
    }
    return render(request, 'temp_app/init_sensor.html', context)


def init_db(request):
    return render(request, 'temp_app/init_db.html')


# Views for Forms


def create_chat_user(request):
    data = request.GET
    try:

        bot = ChatUser(
            username=data.get('username'),
            bot_token=data.get('bot_token'),
            chat_id=data.get('chat_id'),
        )
        bot.save()

        context = {
            "url": "/settings",
            "status": "Success",
        }

        return render(request, 'temp_app/redirect.html', context)
    except Exception as e:
        return render(request, e)


def update_chat_user(request):
    data = request.GET
    chat_user = get_object_or_404(ChatUser, pk=data.get('pk'))

    try:
        chat_user.username = data.get('username')
        chat_user.bot_token = data.get('bot_token')
        chat_user.chat_id = data.get('chat_id')
        chat_user.save()

        context = {
            "url": "/settings",
            "status": "Success",
        }

        return render(request, 'temp_app/redirect.html', context)
    except Exception as e:
        return render(request, e)


def create_place(request):
    data = request.GET
    chat_user = get_object_or_404(ChatUser, pk=data.get('foreign_pk'))

    try:
        place = Place(
            zip_code=data.get('zip_code'),
            country_code=data.get('country_code'),
            name=data.get('name'),
        )
        place.save()
        # Add owner
        place.owner.add(chat_user)
        place.save()

        context = {
            "url": "/settings",
            "status": "Success",
        }

        return render(request, 'temp_app/redirect.html', context)
    except Exception as e:
        return render(request, e)


def update_place(request):
    data = request.GET
    place = get_object_or_404(Place, pk=data.get('pk'))
    chat_user = get_object_or_404(ChatUser, pk=data.get('foreign_pk'))

    try:

        place.room = data.get('room_pk')
        place.zip_code = data.get('zip_code')
        place.country_code = data.get('country_code')
        place.name = data.get('name')
        place.owner.add(chat_user)
        place.save()

        context = {
            "url": "/settings",
            "status": "Success",
        }

        return render(request, 'temp_app/redirect.html', context)
    except Exception as e:
        message = ""
        for arg in e.args:
            message += arg
        return Http404(message)


def create_room(request):
    data = request.GET
    place = get_object_or_404(Place, pk=data.get('foreign_pk'))

    try:
        place_pk = data.get('foreign_pk')
        room = Room(
            place=place,
            room_type=data.get('room_type'),
            name=data.get('name'),
        )
        room.save()

        context = {
            "url": "/settings",
            "status": "Success",
        }

        return render(request, 'temp_app/redirect.html', context)
    except Exception as e:
        return Http404()


def update_room(request):
    data = request.GET
    room = get_object_or_404(Room, pk=data.get('pk'))
    place = get_object_or_404(Place, pk=data.get('foreign_pk'))

    try:

        room.place = place
        room.room_type = data.get('room_type')
        room.name = data.get('name')
        room.save()

        context = {
            "url": "/settings",
            "status": "Success",
        }

        return render(request, 'temp_app/redirect.html', context)
    except Exception as e:
        return render(request, e)


def create_sensor(request):
    data = request.GET
    room_pk = data.get('room_pk')
    try:
        new_sensor = Sensor(
            name=data.get('sensor_name'),
            room=Room.objects.get(pk=room_pk),
            ip=data.get('entry_ip'),
        )
        new_sensor.save()

        # change sensor for all entries with this ip
        entries = Entrie.objects.filter(ip=data.get('entry_ip'))
        for entrie in entries:
            entrie.sensor = new_sensor
            entrie.save()

        context = {
            "url": "/settings",
            "status": "Success",
        }

        return render(request, 'temp_app/redirect.html', context)
    except Exception as e:
        return render(request, e)


def update_settings(request):
    settings = get_settings()
    data = request.GET

    for key, value in data.items():
        settings[key]['value'] = value

    set_settings(settings)

    context = {
        "url": "/settings",
        "status": "Success",
    }
    return render(request, 'temp_app/redirect.html', context)
