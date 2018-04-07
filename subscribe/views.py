from django.shortcuts import render, get_object_or_404, _get_queryset
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from utils.helper import is_valid_email
from .models import Location, User


def index(request):
    all_locations = Location.objects.all()
    return render(request, 'subscribe/index.html', {'all_locations': sorted(all_locations)})


def subscribe(request):
    u_email = request.POST['email']
    u_location = request.POST['location']
    if not is_valid_email(u_email):
        return HttpResponseNotFound('<h1>Please enter a valid email address</h1>')
    location = get_object_or_404(Location, name=u_location)
    try:
        user = User.objects.get(email=u_email)
    except ObjectDoesNotExist:
        user = User()
        user.email = request.POST['email']
        user.location = location
        user.save()
        return render(request, 'subscribe/success.html', {'user': user})
    else:
        return render(request, 'subscribe/fail.html', {'user': user})
