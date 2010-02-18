from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from business.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from datetime import *
from django.core.mail import send_mail
from django import forms
from django.db.models import Q


# Dashboard-ul unui client
@login_required
def dashboard(request, client_id):
	user = request.user
	client = Client.objects.get(id=client_id)
	
	# Get list of logins
	logins = Login.objects.filter(client = client.pk)
	# Get list of stations
	stations = Station.objects.filter(client = client.pk)
	# Get logiktray
	try:
		logiktray = LogikTrayClient.objects.get(client = client.pk)
	except LogikTrayClient.DoesNotExist:
		logiktray = None
		
	# Get comments
	comments = Comment.objects.filter(client = client.pk).order_by("-datetime")
	
	# Get worktimes
	worktimes = WorkTime.objects.filter(client = client.pk).order_by("-date")
	
	# Get logikpos licences
	logikposlicences = LogikPosLicence.objects.filter(client = client.pk)
	
	return render_to_response('dashboard.html', ({
				'username' : user.username,
				'client' : client, 
				'logins' : logins,
				'stations' : stations,
				'logiktray' : logiktray,
				'comments' : comments,
				'worktimes' : worktimes,
				'logikposlicences' : logikposlicences,
				}))	

# formul pentru filtrarea clientilor in pagina cu dashboard-uri
class ClientFilterForm(forms.Form):
	search = forms.CharField(max_length = 100, widget=forms.TextInput(attrs={'size':'70'}), help_text = 'Cauta in denumire, firma, informatii, contact', required=False)
	city = forms.MultipleChoiceField(choices = Client.objects.values_list('city', 'city').distinct().order_by('city') , widget = forms.CheckboxSelectMultiple, required=False)
	type = forms.MultipleChoiceField(choices = Client.objects.values_list('type', 'type').distinct().order_by('type') , widget = forms.CheckboxSelectMultiple, required=False)
	
# Dashboard-ul unui client
@login_required
def dashboards(request):
	username = request.user.username
	logiktrayclients = LogikTrayClient.objects.select_related().filter(last_online__gte=(datetime.now() + timedelta(0,-600))).order_by("client__name")
	clients = Client.objects.all()
	
	if request.method == 'POST':
		form = ClientFilterForm(request.POST)
	else:
		form = ClientFilterForm(initial = {})
	
	
	advanced = False
	
	if form.is_valid():
		clients = clients.filter(Q(name__icontains = form.cleaned_data["search"]) | 
								 Q(company__icontains = form.cleaned_data["search"]) | 
								 Q(contact__icontains = form.cleaned_data["search"]) | 
								 Q(information__icontains = form.cleaned_data["search"]))
								 
		if len(form.cleaned_data["city"]) > 0:
			clients =clients.filter(Q(city__in = form.cleaned_data["city"]))
			advanced = True
		
		if len(form.cleaned_data["type"]) > 0:
			clients = clients.filter(Q(type__in = form.cleaned_data["type"]))
			advanced = True
	
	clients = clients.order_by("name")
	
	return render_to_response('dashboards.html', ({'username' : username, 'logiktrayclients' : logiktrayclients,
												'clients' : clients, 
												'form' : form,
												'advanced' : advanced
											 }))
	