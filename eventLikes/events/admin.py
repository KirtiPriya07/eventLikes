from django.contrib import admin

# Register your models here.
from .models import Event, EventLike


class EventLikeAdmin(admin.TabularInline):
    model = EventLike

class EventAdmin(admin.ModelAdmin):
    inlines = [EventLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email']
    class Meta:
        model = Event

admin.site.register(Event)
