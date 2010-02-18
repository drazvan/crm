import reporting
from django.db.models import Sum, Avg, Count
from models import *

class WorkTimesReport(reporting.Report):
    model = WorkTime
    verbose_name = 'Work times report'
    link = "worktimes"
    
    # Display mode
    list_display = ['date', 'person', 'client',  'hours', 'description']
    
    # Group mode
    group_by = [ 
        'None', 
        'client', 
        'person', 
        'project',
    ]
    
    annotate = (                    
        ('id', Count, 'Times'),      
        ('hours', Sum, 'Hours'),            
    )
    
    # Detail mode 
    detail_list_display = list_display
    
    # Aggregate and filter
    aggregate = (                  
        ('id', Count, 'Times'),
        ('hours', Sum, 'Hours'),
    )
    
    list_filter = [                #
       'person',
       'client', 
       'project',
       'client__city',
    ]
    
    date_filter = [
        'date',
    ]


class TasksReport(reporting.Report):
    model = Task
    verbose_name = 'Tasks report'
    link = "tasks"
    
    # Display mode
    list_display = ['due_date', 'priority', 'title', 'assigned_to', 'type', 'status', 'owner']
    
    # Group mode
    group_by = [ 
        'None', 
        'assigned_to', 
        'owner',
        'project', 
        'client',
    ]
    
    annotate = (                    
        ('id', Count, 'Count'),                  
    )
    
    # Detail mode 
    detail_list_display = list_display
    
    # Aggregate and filter
    aggregate = (                  
        ('id', Count, 'Count'),
    )
    
    list_filter = [              #
       'assigned_to', 'owner', 'status', 'type', 'priority', 'owner', 'project', 'client', 'client__city', 
    ]
    
    date_filter = [
        'due_date',
    ]
    

class WorkReport(reporting.Report):
    model = Work
    verbose_name = 'Work report'
    link = "work"
    
    # Display mode
    list_display = ['worktime__date', 'worktime__client', 
                    'billable', 'units', 'work_type__name', 
                    'details', 'cost'
                    ]
    
    # Group mode
    group_by = [ 
        'None', 
        'worktime__client',
        'worktime__project', 
        'worktime__person', 
        'work_type', 
    ]
    
    annotate = (                    
        ('id', Count, 'Count'), 
        ('cost', Sum, 'Cost'), 
        ('bill', Sum, 'Bil'),
        ('unbill', Sum, 'Unbil'),              
    )
    
    # Detail mode 
    detail_list_display = list_display
    
    # Aggregate and filter
    aggregate = (                  
        ('id', Count, 'Count'),
        ('cost', Sum, 'Total cost'),
        ('bill', Sum, 'Bil'),
        ('unbill', Sum, 'Unbil'),
    )
    
    list_filter = [                #
       'billable', 
       'work_type',
       'worktime__person',
       'worktime__client', 
       'worktime__client__city', 
       'worktime__project',  
    ]
    
    date_filter = [
        'worktime__date', 
    ]
    
    def cost(self, obj):
        return obj.units * obj.work_type.unit_price
    
    def bill(self, obj):
        if obj.billable:
            return obj.units * obj.work_type.unit_price
        else:
            return 0
    
    def unbill(self, obj):
        if not obj.billable:
            return obj.units * obj.work_type.unit_price
        else:
            return 0
        
class TicketsReport(reporting.Report):
    model = Ticket
    verbose_name = 'Developement tickets report'
    link = "tickets"
    
    # Display mode
    list_display = ['type', 'priority', 'title', 'due_date', 'created_by', 'status', 'release_version']
    
    # Group mode
    group_by = [ 
        'None', 
        'type', 
        'priority',
        'status', 
        'created_by',
        'release_version',
    ]
    
    annotate = (                    
        ('id', Count, 'Count'),                  
    )
    
    # Detail mode 
    detail_list_display = list_display
    
    # Aggregate and filter
    aggregate = (                  
        ('id', Count, 'Count'),
    )
    
    list_filter = [              #
       'type', 'priority', 'status', 'created_by', 'release_version',  
    ]
    
    date_filter = []
    
class ClientsReport(reporting.Report):
    model = Client
    verbose_name = 'Clients report'
    link = "clients"
    
    # Display mode
    list_display = ['name', 'city', 'type', 'subscription', 'company']
    
    # Group mode
    group_by = [ 
        'None', 
        'city', 
        'type',
        'subscription', 
    ]
    
    annotate = (                    
        ('id', Count, 'Count'),                  
    )
    
    # Detail mode 
    detail_list_display = list_display
    
    # Aggregate and filter
    aggregate = (                  
        ('id', Count, 'Count'),
    )
    
    list_filter = [              #
       'city', 'type', 'subscription', 'hide',
    ]
    
    date_filter = []

reporting.register(WorkReport.link, WorkReport) # Do not forget to 'register' your class in reports
reporting.register(WorkTimesReport.link, WorkTimesReport) # Do not forget to 'register' your class in reports
reporting.register(TasksReport.link, TasksReport) # Do not forget to 'register' your class in reports
reporting.register(TicketsReport.link, TicketsReport)
reporting.register(ClientsReport.link, ClientsReport)