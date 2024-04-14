import random
from django.conf import settings
from django.shortcuts import render

from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .forms import EventForm
from .models import Event
from .serializers import (
    EventSerializer, 
    EventActionSerializer,
    EventCreateSerializer
)

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

@api_view(['POST']) # http methos sent by cliet == POST
# @authentication_classes([SessionAuthentication, MyCustomAuth])
@permission_classes([IsAuthenticated])
def event_create_view(request, *args, **kwargs):
    serializer = EventCreateSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def event_detail_view(request, event_id, *args, **kwargs):
    qs = Event.objects.filter(id=event_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = EventSerializer(obj)
    return Response(serializer.data, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def event_delete_view(request, event_id, *args, **kwargs):
    qs = Event.objects.filter(id=event_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this event."}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Event removed"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def event_action_view(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, comment
    '''
    serializer = EventActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        event_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Event.objects.filter(id=event_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = EventSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = EventSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "comment":
            new_comment = Event.objects.create(
                    user=request.user, 
                    parent=obj,
                    content=content,
                    )
            serializer = EventSerializer(new_comment)
            return Response(serializer.data, status=201)
    return Response({}, status=200)





@api_view(['GET'])
def event_list_view(request, *args, **kwargs):
    qs = Event.objects.all()
    serializer = EventSerializer(qs, many=True)
    return Response(serializer.data, status=200)



def event_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.accepts('application/json'):
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = EventForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        # do other form related logic
        obj.user = request.user or None # unkown user
        obj.save()
        if request.accepts('application/json'):
            return JsonResponse(obj.serialize(), status=201) # 201 == created items
        if next_url != None and url_has_allowed_host_and_scheme(next_url, ALLOWED_HOSTS):            
            return redirect(next_url)
        form = EventForm()
    if form.errors:
        if request.accepts('application/json'):
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})



def event_list_view_pure_django(request,*args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Andriod
    return json data
    """
    qs = Event.objects.all()
    events_list =  [x.serialize() for x in qs]
    data = {
        "isUser":False,
        "response": events_list
    }
    return JsonResponse(data)

def event_detail_view_pure_django(request, event_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Andriod
    return json data
    """
    data = {
        "id": event_id,
    }
    status = 200
    try:
        obj = Event.objects.get(id=event_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
    return JsonResponse(data, status=status) # json.dumps content_type='application/json'

