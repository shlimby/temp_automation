from django.http.response import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view


from .models import Entrie, ChatUser, OutsideEntrie, Room, Sensor, Place
from .serializer import EntrieSerializer, ChatUserSerializer, OutsideEntrieSerializer, PlaceSerialiser, RoomSerializer, SensorSerializer


class EntrieViewSet(viewsets.ModelViewSet):
    """REST-API for Entries"""
    queryset = Entrie.objects.all()
    serializer_class = EntrieSerializer

    def get_queryset(self):
        if self.kwargs.get('pk') == None:
            # send maximum of 20 elements
            return super().get_queryset()[0:20]
        else:
            # Send singe element
            return super().get_queryset()

    def create(self, request, *args, **kwargs):
        # Get IP from client
        if request.data.get('ip') == None:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                request.data['ip'] = x_forwarded_for.split(',')[0]
            else:
                request.data['ip'] = request.META.get('REMOTE_ADDR')

        # try find sensor for this ip
        try:
            sensor = Sensor.objects.get(ip=request.data.get('ip'))
            request.data['sensor'] = sensor.pk

            # try fill data
            try:
                # get Outsidedata to this sensor
                latest_outside_data = sensor.room.place.outsideentrie_set.latest(
                    'timestamp')
                request.data['out_data'] = latest_outside_data.pk

                # Check if Window is open
            except:
                pass

        except:
            request.data['sensor'] = None
            pass

        # Create object
        return super().create(request, *args, **kwargs)


class ChatUserViewSet(viewsets.ModelViewSet):
    """REST-API for ChatUser"""
    queryset = ChatUser.objects.all()
    serializer_class = ChatUserSerializer


class SensorViewSet(viewsets.ModelViewSet):
    """REST-API for Sensors"""
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """REST-API for Sensors"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    """REST-API for Sensors"""
    queryset = Place.objects.all()
    serializer_class = PlaceSerialiser


class OutsideEntrieViewSet(viewsets.ModelViewSet):
    """REST-API for Sensors"""
    queryset = OutsideEntrie.objects.all()
    serializer_class = OutsideEntrieSerializer


@api_view(['GET'])
def roomtype_options(request):
    out = Room.room_type_choices
    return JsonResponse(out, safe=False)
