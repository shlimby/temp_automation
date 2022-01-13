from .models import ChatUser, Entrie, OutsideEntrie, Place, Room, Sensor

from rest_framework import routers, serializers, viewsets


class EntrieSerializer(serializers.ModelSerializer):
    """Serializer for Entrie model"""
    class Meta:
        model = Entrie
        fields = '__all__'
        # there are fileds that may not be requiered
        extra_kwargs = {
            'window_open': {'required': False},
            'temp_out_deg': {'required': False},
            'timestamp': {'required': False},
            'ip': {'required': False},
            'sensor': {'required': False},
        }


class ChatUserSerializer(serializers.ModelSerializer):
    """Serializer for ChatUser model"""
    class Meta:
        model = ChatUser
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):
    """Serializer for Sensor model"""
    class Meta:
        model = Sensor
        depth = 4
        fields = '__all__'

    def get_entries(self, obj):
        return EntrieSerializer(obj.entries[:5], many=True).data


class PlaceSerialiser(serializers.ModelSerializer):
    """Serializer for Place model"""
    class Meta:
        model = Place
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model"""
    class Meta:
        model = Room
        fields = '__all__'


class OutsideEntrieSerializer(serializers.ModelSerializer):
    """Serializer for Outside model"""
    class Meta:
        model = OutsideEntrie
        fields = '__all__'
