from django.http import HttpResponse, Http404
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from business.models import *

from datetime import *

def add_timer(request):
    username = request.user.username
    
    # if it's a post then we have to create a new timer
    if request.method == "POST":
        # initialize new timer       
        new_timer = Timer(title = request.POST["new_timer_title"])
        new_timer.last_start = datetime.now()
        new_timer.hours = 0
        
        new_timer.save()
        
    return redirect(to="/crm/timers")

# Stops a timer
def stop_timer(request, id):
    # Try to extract the id
    try:
        id = int(id)
    except ValueError:
        raise Http404()
    
    # update the timer
    timer = Timer.objects.get(id=id)
    timer.hours = 1
    timer.last_start = None
    timer.save()
    
    # return to the timers page
    return redirect(to="/crm/timers")
    


@login_required
def timers(request):
    username = request.user.username
    
    timers = Timer.objects.all()
    
    return render_to_response('timers.html', ({'username' : username, 
                                               'timers' : timers,
                                              }))