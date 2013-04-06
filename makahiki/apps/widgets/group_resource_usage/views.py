"""Provides the view of the widget."""
from apps.managers.resource_mgr.models import ResourceSetting
from apps.managers.resource_mgr import resource_mgr
from apps.managers.team_mgr.models import Group

from datetime import date

def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    
    header_row = ["Group"]
    resources = []
    
    for resource in ResourceSetting.RESOURCE_CHOICE:
        header_row.append(resource[0])
        resources.append(resource[0])
    
    body_rows = []    
    count = -1
    for group in Group.objects.all():
        body_rows.append([group.name])
        count += 1
        for resource in resources:
            usage = resource_mgr.group_resource_usage(date.today(), group, resource)
            body_rows[count].append(usage)        
        
    return {
        "header_row": header_row,
        "body_rows": body_rows,
    }
