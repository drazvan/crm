from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from business.models import *
from mycalendar import *
import reporting


import datetime

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
	
def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)


class MenuItem(object):
	def __init__(self, link, name):
		self.link = link
		self.name = name

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from datetime import *

			 
@login_required
def main(request):
    username = request.user.username
    notifications = Notification.objects.all().filter(datetime__gt=datetime.now() + timedelta(days = -30)).order_by("-datetime");
    logiktrayclients = LogikTrayClient.objects.select_related().filter(last_online__gte=(datetime.now() + timedelta(0,-600))).order_by("client__name")
    tasks = Task.objects.filter(assigned_to=request.user.pk, due_date__lt=(datetime.now() + timedelta(11,0))).filter(status="Open").order_by("due_date")
    favorites = FavoriteReport.objects.filter(user=request.user)
    
    notes = DevelopementNote.objects.all()
    tickets = Ticket.objects.filter(status="In progress")    
        
    return render_to_response('main.html', ({'username' : username, 
                                             'notifications' : notifications, 
                                             'logiktrayclients' : logiktrayclients,
                                             'favorites' : favorites,
                                             'notes' : notes,
                                             'tickets' : tickets,
    									 'tasks' : tasks}))


@login_required
def reports(request):
	username = request.user.username
		
	return render_to_response('reports.html', ({'username' : username, }))

	
@login_required
@permission_required('business.crm.new_licence')
def new_licence(request):
	username = request.user.username
	return render_to_response('main.html', ({'username' : username}))
	
from business.models import LogikTrayClient
from business.models import CRMSetting

def logiktrayversion(request):
	try:
		ltversion = CRMSetting.objects.get(name="LogikTrayVersion")
		return HttpResponse(ltversion.value)
		
	except CRMSetting.DoesNotExist:
		return HttpResponse("-1")


def online(request, clientname):
	username = request.user.username
	clientip = request.META['REMOTE_ADDR'] 
	
	try:
		ltClient = LogikTrayClient.objects.get(name=clientname)
		ltClient.last_online = datetime.now()
		ltClient.ip = clientip
		ltClient.save()
		
	except LogikTrayClient.DoesNotExist:
		newClient = LogikTrayClient.objects.create(name=clientname, ip=clientip, last_online = datetime.now())
		newClient.save();

	
	return render_to_response('online.html', ({'username' : username, 'clientname' : clientname}))
	
from django.core.mail import send_mail


def test_mail(request):
	send_mail('Subject here', 'Here is the message.', 'CRM@logik.ro',
	['drazvan@gmail.com'], fail_silently=False)
	return HttpResponse("Sent.")
	

	
import os
import subprocess

def get_licence(HardwareInfo, Version=2, TipPachet=1, TipAdministrare=1, ALaCarte=True, ServireRapida=False, Catering=False, CodDeBare=False,
				FidelizareClienti=False, Rezervari=False, ModalitatiDePreparare=False, HappyHour=False, 
				ModalitatiDePlata=False, MultiLanguage=False, AnalizaGrafica=False, Facturare=False):
				
	command = "e:\Django\Code\crm\LogikLicenceUtil.exe %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s" % (HardwareInfo, Version, TipPachet, TipAdministrare, ALaCarte, ServireRapida, Catering, CodDeBare,
				FidelizareClienti, Rezervari, ModalitatiDePreparare, HappyHour, ModalitatiDePlata, MultiLanguage, AnalizaGrafica, Facturare)
	
	# Delete the eventual old file
	if os.access('e:\Django\Code\crm\licence.txt', os.F_OK):
		os.remove('e:\Django\Code\crm\licence.txt')

	code = subprocess.call(command)

	if code != 0:
		return "There was an eror: %s.\n" % (code)
		
	licence = None

	try:
		fin = open("e:\Django\Code\crm\licence.txt")
		licence = fin.readline()
		fin.close()
	except IOError, e:
		return "IO error: %s " % (e)
	
	return licence
				
				
def test_licence(request):
	return HttpResponse(get_licence('1261-20944-64511'))
	
@login_required
def calendar(request, year = datetime.now().date().year, month=datetime.now().date().month):
	return render_to_response('calendar.html', month_cal(request, int(year), int(month)))
	
@login_required
def logikpos(request):
	username = request.user.username
	
	bugs = Ticket.objects.filter(status__gte='Completed', type='Bug').order_by('priority')
	features = Ticket.objects.filter(status__gte='Completed', type='New Feature').order_by('priority')
	improvements = Ticket.objects.filter(status__gte='Completed', type='Improvement').order_by('priority')
	
	in_progresses = Ticket.objects.filter(status='In progress').order_by('priority')
		
	return render_to_response('logikpos.html', ({'username' : username, 
												 'bugs' : bugs, 
												 'features' : features,
												 'improvements' : improvements,
												 'in_progresses' : in_progresses,
												}))
from django.utils.http import urlencode
  
@login_required
def reports(request):
    reports = reporting.all_reports()
    favorites = FavoriteReport.objects.filter(user=request.user)
    username = request.user.username
    
    return render_to_response('reports.html', {'reports': reports, 'favorites' : favorites, 
                                               'username' : username}, 
                              context_instance=RequestContext(request))  
  
@login_required
def favorite_report(request):
    username = request.user.username
    
    params = urlencode(request.GET)
    link = request.GET["link"]
    
    return render_to_response('favorite_report.html', ({'username' : username, 
                                                        'params' : params,
                                                        'link' : link,
                                                }))
    
@login_required
def save_report(request):
    user = request.user
    title = request.POST["title"]
    params = request.POST["params"]
    link = request.POST["link"]

    username = user.username
    
    report = FavoriteReport(user=user, title=title, url="/crm/reporting/" + link + "/?" + params)
    report.save()
           
    return render_to_response('message.html', ({'username' : username, 
                                                'message' : "Report saved successfully."
                                                }))
    
def reminder_tick(request):
    reminders = Reminder.objects.filter(date_time__lt=datetime.now(), passed=False)
    
    for reminder in reminders:
        send_mail('CRM Reminder: %s ' % (reminder.message) , 
        '%s' % (reminder.message), 'CRM@logik.ro',
        [reminder.person.email], fail_silently=False)
        reminder.passed=True
        reminder.save()
         
    return HttpResponse("ok")
        