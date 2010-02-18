from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf.urls.defaults import *

import reporting

from crm.views.views import *
from crm.dashboard import *
from crm.reports import *
from views.timers import *

admin.autodiscover()
reporting.autodiscover()                                   # autodiscover reports in applications


urlpatterns = patterns('',
    (r'^$', main),
	(r'^register/$', new_licence), 
    (r'^hello/$', hello),
    (r'^time/$', current_datetime),
    (r'^time/plus/(\d{1,2})/$', hours_ahead),
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),
	(r'^login/$',  login),
    (r'^logout/$', logout),
	(r'^online/([^/]+)/$', online),
	(r'^logiktrayversion/$', logiktrayversion),
	(r'^testmail/$', test_mail),
	(r'^testlicence/$', test_licence),
	(r'^dashboard/([^/]+)/$', dashboard),
	(r'^dashboards/$', dashboards),
	(r'^calendar/([^/]+)/([^/]+)/$', calendar),
	(r'^calendar/$', calendar),
	(r'^developement/$', logikpos),
	(r'^reports/$', reports), 
	(r'^reports/worksummary/$', worksummary), 
	(r'^reporting/', include('reporting.urls')),
    (r'^timers/$', timers),
    (r'^timers/add$', add_timer),
    (r'^timers/stop/(\d{1,2})/$', stop_timer),
    (r'^save_report/$', save_report),
    (r'^favorite_report/$', favorite_report),
    (r'^reports/$', reports),
    (r'^remindertick/$', reminder_tick),
    
    # Some work around as i cannot map the development server on a directory such as /crm
    
    (r'^crm/$', main),
    (r'^crm/register/$', new_licence), 
    (r'^crm/hello/$', hello),
    (r'^crm/time/$', current_datetime),
    (r'^crm/time/plus/(\d{1,2})/$', hours_ahead),
    (r'^crm/admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^crm/admin/', include(admin.site.urls)),
    (r'^crm/login/$',  login),
    (r'^crm/logout/$', logout),
    (r'^crm/online/([^/]+)/$', online),
    (r'^crm/logiktrayversion/$', logiktrayversion),
    (r'^crm/testmail/$', test_mail),
    (r'^crm/testlicence/$', test_licence),
    (r'^crm/dashboard/([^/]+)/$', dashboard),
    (r'^crm/dashboards/$', dashboards),
    (r'^crm/calendar/([^/]+)/([^/]+)/$', calendar),
    (r'^crm/calendar/$', calendar),
    (r'^crm/developement/$', logikpos),
    (r'^crm/reports/$', reports), 
    (r'^crm/reports/worksummary/$', worksummary), 
    (r'^crm/reporting/', include('reporting.urls')),
    (r'^crm/timers/$', timers),
    (r'^crm/timers/add$', add_timer),
    (r'^crm/timers/stop/(\d{1,2})/$', stop_timer),
    (r'^crm/save_report/$', save_report),
    (r'^crm/favorite_report/$', favorite_report),
    (r'^crm/reports/$', reports),
    (r'^crm/remindertick/$', reminder_tick),
)
