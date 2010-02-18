from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from business.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from datetime import *
from django.core.mail import send_mail
from django import forms
from django.db.models import Q
from django.forms import extras

# formul pentru filtrarea clientilor in pagina cu dashboard-uri
class WorkSummaryFilterForm(forms.Form):
	name = forms.CharField() 
	end_date = forms.DateTimeField(widget = extras.SelectDateWidget())
	start_date = forms.DateTimeField(widget = forms.DateInput())
	search = forms.CharField(max_length = 100, widget=forms.TextInput(attrs={'size':'70'}), help_text = 'Cauta in denumire, firma, informatii, contact', required=False)
	city = forms.MultipleChoiceField(choices = Client.objects.values_list('city', 'city').distinct().order_by('city') , widget = forms.CheckboxSelectMultiple, required=False)
	type = forms.MultipleChoiceField(choices = Client.objects.values_list('type', 'type').distinct().order_by('type') , widget = forms.CheckboxSelectMultiple, required=False)
	
# Dashboard-ul unui client
@login_required
def worksummary(request):
	username = request.user.username
	logiktrayclients = LogikTrayClient.objects.select_related().filter(last_online__gte=(datetime.now() + timedelta(0,-600))).order_by("client__name")
	clients = Client.objects.all()
	
	if request.method == 'POST':
		form = WorkSummaryFilterForm(request.POST)
	else:
		form = WorkSummaryFilterForm(initial = {})
	
	
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
	
	return render_to_response('worksummary.html', ({'username' : username, 'logiktrayclients' : logiktrayclients,
												'clients' : clients, 
												'form' : form,
												'advanced' : advanced
											 }))
	