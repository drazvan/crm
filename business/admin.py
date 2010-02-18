from django.contrib import admin
from crm.business.models import *
from django.contrib.auth.models import User
from crm.business.licence import *
from django.core.mail import send_mail
import os
import subprocess

class LoginInlineAdmin(admin.TabularInline):
	model = Login
	extra = 1

class LogikTrayClientAdmin(admin.ModelAdmin):
	list_display = ('name', 'ip', 'is_online', 'last_online', 'client' )
	search_fields = ('name',  )
	
class LogEntryAdmin(admin.ModelAdmin):
	list_display = ('logik_tray_client', 'log_name', 'date', 'type', 'message_name', )
	search_fields = ('logik_tray_client', 'log_name', 'message_name', 'description', )
	list_filter = ('date', 'logik_tray_client', 'type', )
	
	fieldsets = (('General', 
				{'fields': ('logik_tray_client', 'log_name', 'date', 'type', ) }),
			('Details', 
				{'fields': ('message_name', 'description', 'additional_information',)})
			)
			
class StationAdmin(admin.ModelAdmin):
	list_display = ('name', 'type', 'client', 'local_IP', 'additional_information', )
	search_fields = ('name', 'additional_information', )
	list_filter = ('client', 'type', )
	
	fieldsets = (('General', 
				{'fields': ('name', 'type', 'client', ) }),
			('Other information', 
				{'fields': ('local_IP', 'additional_information',)})
			)
	inlines = [
		LoginInlineAdmin,
		]
			
class CRMSettingAdmin(admin.ModelAdmin):
	list_display = ('name', 'value', )
	search_fields = ('name', )
	
class LoginAdmin(admin.ModelAdmin):
	list_display = ('username', 'password', 'station' , 'client', 'description', )
	search_fields = ('username', 'description', 'client__name' )
	list_filter = ('client', )
	
class FranceCallAdmin(admin.ModelAdmin):
	list_display = ('who', 'when', 'duration', 'cost', 'why')
	search_fields = ('who', 'why')
	list_filter = ('who', 'when', )

class ClientAdmin(admin.ModelAdmin):
	list_display = ('name', 'type', 'city', 'subscription', 'contact', 'information')
	search_fields = ('name', 'information', 'company')
	list_filter = ('type', 'city', )
	ordering = ('name', 'city', )
	
	fieldsets = (('General', 
				{'fields': ('name', 'company', 'type', 'city', 'subscription', 'hide')}
				),
			('Details', 
				{'fields': ('contact', 'address', 'information', )})
			)
			
class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ('name', 'information', )
	search_fields = ('name', 'information', )
	ordering = ('name', )
			
def announce_task(user, task):
	send_mail('CRM Task: %s - %s' % (task.status, task.title) , 
	'Owner: %s\n\
	Assigned to: %s \n\
	Title: %s \n\
	Project: %s \n\
	Client: %s \n\
	Start date: %s \n\
	Due date: %s \n\
	Type: %s \n\
	Priority: %s \n\
	Status: %s \n\
	Description: %s ' % 
				(task.owner, task.assigned_to, task.title, task.project, task.client, task.start_date, task.due_date, 
				task.type, task.priority, task.status, task.description), 'CRM@logik.ro',
				[user.email], fail_silently=False)
			
class TaskAdmin(admin.ModelAdmin):
	list_display = ('title', 'project', 'client', 'priority', 'due_date', 'assigned_to', )
	search_fields = ('title',  )
	list_filter = ('project', 'assigned_to', 'priority', 'status', )
	
	fieldsets = ((None, 
				{'fields': ('title', ('project', 'client'), ('type', 'priority', 'status'),
							('start_date', 'due_date', ), 
							('assigned_to', 'owner'), 'description') }),
			)
	def save_model(self, request, obj, form, change):
		super(TaskAdmin, self).save_model(request, obj, form, change)
		
		if request is not None:
			if obj.owner != request.user:
				announce_task(obj.owner, obj)
				request.user.message_set.create(message="Email sent to %s" % (obj.owner.email))
			if obj.assigned_to != request.user:
				announce_task(obj.assigned_to, obj)
				request.user.message_set.create(message="Email sent to %s" % (obj.assigned_to.email))


class WorkInlineAdmin(admin.TabularInline):
	model = Work
	extra = 3

				
class WorkTimeAdmin(admin.ModelAdmin):
	list_display = ('date', 'person', 'hours', 'project', 'client',  'description')
	search_fields = ('description',  )
	list_filter = ('person', 'project',  )

	fieldsets = ((None, 
                            {'fields': ('person', ('project', 'client'), 'date', 'hours',
                                                    'description') }),
                    )
					
	inlines = [
		WorkInlineAdmin,
		]
		
	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		field = super(WorkTimeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
		if db_field.name == u'person' and request is not None:
			field.initial = request.user.pk
		return field
		
class WorkTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'unit_price', 'unit_name')
	search_fields = ('name',  )
	list_filter = ('unit_price', 'unit_name',  )



	
class NotificationAdmin(admin.ModelAdmin):
	list_display = ('datetime', 'owner', 'title', 'description')
	search_fields = ('title', 'description',  )
	list_filter = ('owner', 'datetime',  )

	fieldsets = ((None, 
                            {'fields': ('owner', 'title', 'description') }),
                    )
	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		field = super(NotificationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
		if db_field.name == u'owner' and request is not None:
			field.initial = request.user.pk
		return field
		
	def save_model(self, request, obj, form, change):
		super(NotificationAdmin, self).save_model(request, obj, form, change)
		
		if request is not None:
			for user in User.objects.all():
				send_mail('CRM Notification: %s ' % (obj.title) , 
				'Owner: %s\nTitle: %s\nDescription: %s' % (obj.owner, obj.title, obj.description), 'CRM@logik.ro',
				[user.email], fail_silently=False)
				request.user.message_set.create(message="Email sent to %s" % (user.email))

class CommentAdmin(admin.ModelAdmin):
	list_display = ('datetime', 'owner', 'client', 'text')
	search_fields = ('client__name', 'text',  )
	list_filter = ('owner', 'datetime',  )

	fieldsets = ((None, 
                            {'fields': ('owner', 'client', 'datetime', 'text') }),
                    )
	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		field = super(CommentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
		if db_field.name == u'owner' and request is not None:
			field.initial = request.user.pk
		return field	
		
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
	
class LogikPosLicenceAdmin(admin.ModelAdmin):
	list_display = ('licence', 'client', 'creator', 'tip_pachet', 'tip_administrare')
	search_fields = ('client__name',  )
	list_filter = ('client', 'creation_time',  )

	fieldsets = ((None, 
                            {'fields': ('creator', 'client', 'hardware_info', ) }),
				('Packet', 
                            {'fields': ('tip_pachet', 'tip_administrare', ) }),
				('Activity', 
                            {'fields': (('a_la_carte', 'servire_rapida', 'catering', 'cod_de_bare'),) }),
				('Modules', 
                            {'fields': (('fidelizare_clienti', 'rezervari', 'modalitati_de_preparare', 'happy_hour'), ('modalitati_de_plata', 'multi_language',
										'analiza_grafica', 'facturare')) }),
				('Licence', 
                            {'fields': ('licence',  ) }),
				('Extra', 
                            {'fields': ('additional_information',  ) })
                    )
	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		field = super(LogikPosLicenceAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
		if db_field.name == u'creator' and request is not None:
			field.initial = request.user.pk
		return field	
	
	def save_model(self, request, obj, form, change):
		obj.version = 3
		obj.licence = get_licence(obj.hardware_info, obj.version, obj.tip_pachet, obj.tip_administrare, 
							obj.a_la_carte, obj.servire_rapida, obj.catering, obj.cod_de_bare,
							obj.fidelizare_clienti, obj.rezervari, obj.modalitati_de_preparare, obj.happy_hour,
							obj.modalitati_de_plata, obj.multi_language, obj.analiza_grafica, obj.facturare)
							
		super(LogikPosLicenceAdmin, self).save_model(request, obj, form, change)	

class LogikPosVersionAdmin(admin.ModelAdmin):
	list_display = ('number', 'release_date', 'description')
	search_fields = ('description',  'number')
	list_filter = ('release_date',  )

class TicketAdmin(admin.ModelAdmin):
	list_display = ('title', 'type', 'priority', 'due_date',)
	search_fields = ('title', 'description'  )
	list_filter = ('type', 'priority', 'status',  )

	fieldsets = ((None, 
                            {'fields': ('title', ('type', 'priority'), 'due_date', 'description', 'created_by') }),
				('Reserved fields (filled during and after developement)', 
                            {'fields': ('status', 'completion_date', 'completion_comment', 'release_version') }),
                    )
					
	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		field = super(TicketAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
		if db_field.name == u'created_by' and request is not None:
			field.initial = request.user.pk
		return field	
	
	def save_model(self, request, obj, form, change):							
		super(TicketAdmin, self).save_model(request, obj, form, change)
		
		if request is not None:
			user = User.objects.get(id=1)
			send_mail('CRM Ticket: %s ' % (obj.title) , 
			'Owner: %s\nTitle: %s\nDescription: %s' % (obj.created_by, obj.title, obj.description), 'CRM@logik.ro',
			[user.email], fail_silently=False)
			request.user.message_set.create(message="Email sent to %s" % (user.email))
		
class TimerAdmin(admin.ModelAdmin):
	list_display = ('title', 'hours', 'last_start', 'description')
	list_filter = ('last_start',  )

class FavoriteReportAdmin(admin.ModelAdmin):
	list_display = ('user', 'title', )
	list_filter = ('user',  )
	
class DevelopementNoteAdmin(admin.ModelAdmin):
	list_display = ('text', )
	
	
class ReminderAdmin(admin.ModelAdmin):
	list_display = ('message', 'person', 'date_time', 'passed')
	search_fields = ('message',  )
	list_filter = ('person', 'passed',  )
	
	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		field = super(ReminderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
		if db_field.name == u'person' and request is not None:
			field.initial = request.user.pk
		return field


admin.site.register(CRM)
admin.site.register(CRMSetting, CRMSettingAdmin)
admin.site.register(LogikTrayClient, LogikTrayClientAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Login, LoginAdmin)
admin.site.register(FranceCall, FranceCallAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Project)
admin.site.register(WorkTime, WorkTimeAdmin)
admin.site.register(WorkType, WorkTypeAdmin)
admin.site.register(Work)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(LogikPosLicence, LogikPosLicenceAdmin)
admin.site.register(LogikPosVersion, LogikPosVersionAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Timer, TimerAdmin)
admin.site.register(FavoriteReport, FavoriteReportAdmin)
admin.site.register(Reminder, ReminderAdmin)
admin.site.register(DevelopementNote, DevelopementNoteAdmin)

