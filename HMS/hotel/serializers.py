from rest_framework import serializers
from .models import Room, Booking


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def to_representation(self, instance):
        if self.context['request'].user == instance.user or self.context['request'].user.is_staff:
            return super().to_representation(instance)
        else:
            return {'id': instance.id}