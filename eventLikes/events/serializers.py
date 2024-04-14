from django.conf import settings
from rest_framework import serializers
from .models import Event

MAX_EVENT_LENGTH = settings.MAX_EVENT_LENGTH
EVENT_ACTION_OPTIONS = settings.EVENT_ACTION_OPTIONS


class EventActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip() # "Like " -> "like"
        if not value in EVENT_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action to reate an event.")
        return value



class EventCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'content', 'likes']
    
    def get_likes(self, obj):
        return obj.likes.count()
    
    def validate_content(self, value):
        if len(value) > MAX_EVENT_LENGTH:
            raise serializers.ValidationError("This event details is too long")
        return value




class EventSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    og_event = EventCreateSerializer(source='parent', read_only=True)
    class Meta:
        model = Event
        fields = ['id', 'content', 'likes', 'is_comment', 'og_event']
    def get_likes(self, obj):
        return obj.likes.count()

    