# Template tag
from datetime import date, timedelta
from business.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def get_last_day_of_month(year, month):
    if (month == 12):
        year += 1
        month = 1
    else:
        month += 1
    return date(year, month, 1) - timedelta(1)

def month_cal(request, year, month):
    
    include_tasks = True
    include_reminders = True
    include_tickets = True
    
    selected_users = ["-1"]
    for user in User.objects.all():
        selected_users.append(str(user.id))
    
    if request.method == "POST":
        if not "include_tasks" in request.POST:
            include_tasks = False
        if not "include_reminders" in request.POST:
            include_reminders = False
        if not "include_tickets" in request.POST:
            include_tickets = False
        if "user__in" in request.POST:
            selected_users = []
            selected_users = dict(request.POST.lists())["user__in"]
            
    users = []
    users.append((-1, "(all)", ("Yes" if str(-1) in selected_users else "No")))
    for user in User.objects.all():
        users.append((user.id, user.username, ("Yes" if str(user.id) in selected_users else "No")))
    
    user_ids = [int(id) for id in selected_users]
    
    # Tasks that are due this month
    task_list = Task.objects.filter(due_date__year=year, due_date__month=month, status="Open", assigned_to__id__in=user_ids)
    reminders = Reminder.objects.filter(date_time__year=year, date_time__month=month, person__id__in=user_ids)
    tickets = Ticket.objects.filter(due_date__year=year, due_date__month=month)
   
    # Prepare calendar
    first_day_of_month = date(year, month, 1)
    last_day_of_month = get_last_day_of_month(year, month)
    first_day_of_calendar = first_day_of_month - timedelta(first_day_of_month.weekday())
    last_day_of_calendar = last_day_of_month + timedelta(7 - last_day_of_month.weekday())

    month_cal = []
    week = []

    i = 0
    day = first_day_of_calendar
    while day <= last_day_of_calendar:
        cal_day = {}
        cal_day['day'] = day
        cal_day['task_list'] = []
        cal_day['reminders'] = []
        cal_day['tickets'] = []
		
        # add things to current day
        if include_tasks:
            for task in task_list:
                if task.due_date == day:
                   cal_day['task_list'].append(task)
            
        if include_reminders:       
            for reminder in reminders:
                if reminder.date_time.date() == day:
                    cal_day['reminders'].append(reminder)

        if include_tickets:
            for ticket in tickets:
                if ticket.due_date == day:
                   cal_day['tickets'].append(ticket)
        
        # Other stuff
        if day.month == month:
            cal_day['in_month'] = True
        else:
            cal_day['in_month'] = False  
        
        if day.weekday() == 5 or day.weekday() == 6:
            cal_day['weekend'] = True
        else:
            cal_day['weekend'] = False

        if day == datetime.now().date():
            cal_day['today'] = True
        else:
            cal_day['today'] = False
			
        week.append(cal_day)
				
        if day.weekday() == 6:
            month_cal.append(week)
            week = []
        i += 1
        day += timedelta(1)
        next_month = month + 1
        next_year = year
        if next_month == 13:
            next_month = 1
            next_year += 1
			
        prev_month = month - 1
        prev_year = year
        if prev_month == 0:
            prev_month = 12
            prev_year -= 1
        first_day_of_month = date(year, month, 1)


    return {'calendar': month_cal, 
			'month': month, 'year' : year, 
            'include_tasks' : include_tasks,
            'include_reminders' : include_reminders,
            'include_tickets' : include_tickets,
            'users' : users,
			'next_month': next_month, 'next_year' : next_year,
			'prev_month': prev_month, 'prev_year' : prev_year,
			'first_day_of_month': first_day_of_month}




