from django.db import models
from django.contrib.auth.models import User
from datetime import *

# General class
class CRM(models.Model):
	name = models.CharField(max_length=30)
	class Meta:
		permissions = (
			("new_licence", "Register new licence"),
			("view_logs", "Visualize logs"),
			("request_ops", "Request client operations"),
			("update_db", "Update database"),
	)

# Un tip de abonament
class Subscription(models.Model):
	name = models.CharField(max_length = 100, help_text = "Numele tipului de abonament")
	information = models.TextField(help_text = "Orice informatii suplimentare despre abonament", blank = True, null = True)
	
	def __unicode__(self):
		return u'%s' % (self.name)

class Client(models.Model):
	class Meta:
		ordering = ['name']
	
	name = models.CharField(max_length=100, help_text = 'Numele locatiei')
	address = models.CharField(max_length=100, blank=True)
	city = models.CharField(max_length=100)
	information = models.TextField(blank=True, help_text = 'Orice alte informatii')
	type = models.CharField(max_length=30, help_text = 'Bar, Cafenea, Cantina, etc.')
	company = models.CharField(max_length = 100, help_text = 'Numele firmei "SC ... "', blank=True, null = True)
	contact = models.TextField(blank = True, null = True)
	subscription = models.ForeignKey(Subscription, blank = True, null = True)
	hide = models.NullBooleanField(default=False)
	
	def __unicode__(self):
		return u'%s - %s' % (self.name, self.city)
		
class Login(models.Model):
	username = models.CharField(blank=True, max_length=50)
	password = models.CharField(max_length=50)
	description = models.CharField(blank=True, max_length=200)
	station = models.ForeignKey('Station', related_name = "logins", blank=True, null=True)
	client = models.ForeignKey(Client, blank=True, null=True)
	
	def __unicode__(self):
		return u'%s - %s' % (self.username, self.description)
		
# A logik tray instance
class LogikTrayClient(models.Model):
	name = models.CharField(max_length=30)
	ip = models.CharField(max_length=15)
	last_online = models.DateTimeField(blank=True, null=True)
	client = models.ForeignKey(Client, blank=True, null=True)
	
	ordering = [name]
	
	def is_online(self):
		if self.last_online is None:
			return "No"
		if (datetime.now() - self.last_online) < timedelta(0, 600):
			return "Yes"
		return "No"
		
	is_online.short_description = 'Is Online?'
	
	def __unicode__(self):
		return u'%s' % (self.name)

class Station(models.Model):
	name = models.CharField(max_length=30)
	type = models.CharField(max_length=30, help_text = 'POS, Calculator birou, Server, etc.')
	client = models.ForeignKey(Client)
	local_IP = models.CharField(max_length=15, blank=True, null=True)
	login = models.ForeignKey(Login, related_name='stations', blank=True, null=True)
	additional_information = models.TextField(blank=True, null=True)
	
	def __unicode__(self):
		return u'%s @ %s' % (self.name, self.client)
	
class CRMSetting(models.Model):
	name = models.CharField(max_length=30)
	value = models.CharField(max_length=100)
	
	def __unicode__(self):
		return u'%s=%s' % (self.name, self.value)
		
# An entry from LogikPOS log
class LogEntry(models.Model):
	logik_tray_client = models.ForeignKey(LogikTrayClient)
	log_name = models.CharField(max_length=30)
	date = models.DateTimeField()
	type = models.CharField(max_length=50)
	message_name = models.CharField(max_length=50)
	description = models.TextField()
	additional_information = models.TextField()
	
	def __unicode__(self):
		return u'[%s] %s - %s' % (self.date, self.log_name, self.type)
		
# A call made from someone to razvan		
class FranceCall(models.Model):
	who = models.CharField(max_length=50)
	when = models.DateTimeField()
	duration = models.CharField(max_length=20)
	cost = models.FloatField()
	why = models.TextField()
	
	def __unicode__(self):
		return u'%s %s %s' % (self.who, self.when, self.duration)
		
# A project
class Project(models.Model):
	class Meta:
		ordering = ['name']
		
	name = models.CharField(max_length = 100)
	description = models.TextField(blank = True, null = True)
	
	def __unicode__(self):
		return u'%s' % (self.name)
		
# A task
class Task(models.Model):
	PRIORITY_CHOICES = (
		('C', 'Critical'),
		('H', 'High'),
		('M', 'Medium'),
		('L', 'Low'),
	)
	
	TYPE_CHOICES = (
		('Bug', 'Bug'),
		('Feature', 'Feature'),
		('Improvement', 'Improvement'),
		('Test', 'Test'),
		('Other', 'Other'),
	)
	
	STATUS_CHOICES = (
		('Open', 'Open'),
		('Closed', 'Closed'),
	)

	title = models.CharField(max_length = 100)
	client = models.ForeignKey(Client, blank = True, null = True)
	start_date = models.DateField(blank = True, null = True, default=datetime.now().date())
	due_date = models.DateField(blank = True, null = True, default=datetime.now().date() + timedelta(7, 0))
	owner = models.ForeignKey(User, related_name = 'owners')
	assigned_to = models.ForeignKey(User, related_name='users')
	project = models.ForeignKey(Project)
	description = models.TextField(blank = True, null = True)
	priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, null=True, default='M')
	type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, default='Open')

	def __unicode__(self):
		return u'%s' % (self.title)

# Reprezinta un tip de lucru ce se poate face la cineva
class WorkType(models.Model):
	UNIT_NAME_CHOICES = (
		('Hour', 'Hour'),
		('Unit', 'Unit'),
	)
	name = models.CharField(max_length = 100)
	unit_price = models.FloatField(help_text='In euro')
	unit_name = models.CharField(max_length=10, choices = UNIT_NAME_CHOICES)
	def __unicode__(self):
		return u'%s: %s euro per %s' % (self.name, self.unit_price, self.unit_name)

	
class WorkTime(models.Model):
    person = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    client = models.ForeignKey(Client, blank=True, null=True)
    date = models.DateField(default=datetime.now().date())
    hours = models.FloatField(default=0.5, null=True)
    description = models.TextField()
	
    def __unicode__(self):
        return u'%s: %s, %s, %s %s ' % (self.person, self.date, self.hours, 
                                    self.project, self.client)

# reprezinta ceva facut intr-un work time
class Work(models.Model):
	worktime = models.ForeignKey(WorkTime, related_name = "works")
	billable = models.BooleanField()
	units = models.FloatField()
	work_type = models.ForeignKey(WorkType)
	details = models.CharField(max_length = 100, blank=True, null=True)
	
	def __unicode__(self):
		return u'%s, %s x %s, %s %s' % (self.billable, self.units, self.work_type, self.worktime.date, self.worktime.client)
	
class Notification(models.Model):
    owner = models.ForeignKey(User)
    datetime = models.DateTimeField(default=datetime.now())
    title = models.CharField(max_length = 200)
    description = models.TextField()
    
    def __unicode__(self):
        return u'%s' % (self.title)
		
class Comment(models.Model):
	owner = models.ForeignKey(User)
	datetime = models.DateTimeField(default=datetime.now())
	client = models.ForeignKey(Client)
	text = models.TextField()
    
	def __unicode__(self):
		return u'%s - %s' % (self.client, self.text )
	
class DevelopementNote(models.Model):
	text = models.TextField()
	    
	def __unicode__(self):
		return u'%s' % (self.text)
	
class Reminder(models.Model):
	message = models.CharField(max_length=200)
	person = models.ForeignKey(User)
	date_time = models.DateTimeField()
	passed = models.BooleanField()
	
	def __unicode__(self):
		return u'%s to %s: %s' % (self.date_time, self.person, self. message)
	
		
class LogikPosLicence(models.Model):
	creator = models.ForeignKey(User)
	creation_time = models.DateTimeField(default=datetime.now())
	client = models.ForeignKey(Client)
	hardware_info = models.CharField(max_length=25, null=True)
	version = models.IntegerField()
	
	PACHET_CHOICES = (
		(1, 'Logik Basic'),
		(2, 'Logik Avansat'),
		(3, 'Logik Pro'),
	)
	
	ADMINISTRARE_CHOICES = (
		(1, 'Administrare Minim'),
		(2, 'Administrare Basic'),
		(3, 'Administrare Avansat'),
	)
	
	tip_pachet = models.IntegerField(choices=PACHET_CHOICES)
	tip_administrare = models.IntegerField(choices=ADMINISTRARE_CHOICES)

	a_la_carte = models.BooleanField();
	servire_rapida = models.BooleanField();
	catering = models.BooleanField();
	cod_de_bare = models.BooleanField();

	fidelizare_clienti = models.BooleanField();
	rezervari = models.BooleanField();
	modalitati_de_preparare = models.BooleanField();
	happy_hour = models.BooleanField();
	modalitati_de_plata = models.BooleanField();
	multi_language = models.BooleanField();
	analiza_grafica = models.BooleanField();
	facturare = models.BooleanField();

	licence = models.CharField(max_length=50, default=' ')
	
	additional_information = models.TextField()
    
	def __unicode__(self):
		return u'%s - %s' % (self.client, self.licence )

# A LogikPOS version
class LogikPosVersion(models.Model):
	number = models.CharField(max_length = 15)
	release_date = models.DateField()
	description = models.TextField()
	
	def __unicode__(self):
		return u'%s' % (self.number)

# A LogikPOS developement ticket		
class Ticket(models.Model):
	PRIORITY_CHOICES = (
			('Critical', 'Critical'),
			('High', 'High'),
			('Medium', 'Medium'),
			('Very Low', 'Very Low'),
		)

	TYPE_CHOICES = (
			('New Feature', 'New Feature'),
			('Improvement', 'Improvement'),
			('Bug', 'Bug'),
		)
	
	STATUS_CHOICES = (
			('Waiting', 'Waiting'),
			('In progress', 'In progress'), 
			('Completed', 'Completed')
		)
		
	title = models.CharField(max_length = 200)
	type = models.CharField(max_length = 15, choices = TYPE_CHOICES)
	priority = models.CharField(max_length = 15, choices = PRIORITY_CHOICES)
	due_date = models.DateField(blank = True, null = True)
	description = models.TextField()
	
	created_by = models.ForeignKey(User)
	
	status = models.CharField(max_length = 15, choices = STATUS_CHOICES, default='Waiting')
	completion_date = models.DateField(blank = True, null = True)
	completion_comment = models.TextField(blank = True, null = True)
	release_version = models.ForeignKey(LogikPosVersion, blank = True, null = True)

# Timer class used for time management
class Timer(models.Model):
	title = models.CharField(max_length = 200, help_text = "The subject of the timer.")
	hours = models.FloatField(help_text = 'Total number of hours. Updated at stops.', blank=True, null=True)
	last_start = models.DateTimeField( blank=True, null=True)
	description = models.TextField( blank=True, null=True)
	
	def __unicode__(self):
		return "%s %s" % (self.title, self.hours)
	
class FavoriteReport(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length = 200, help_text = "The title of the report.")
	url = models.TextField( blank=True, null=True)
	
	def __unicode__(self):
		return "%s" % (self.title)	
	