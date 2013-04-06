"""Provide the view for the Hello_World widget."""
from apps.managers.score_mgr import score_mgr
from apps.managers.team_mgr.models import Group


def supply(request, page_name):
    """Supply group_scores which is list of [group, score] tuples"""
    _ = page_name
    
    group_scores = []
    for group in Group.objects.all():
        group_scores.append([group.name, score_mgr.group_points(group)])
    
    group_scores.sort(key=lambda tup: tup[1], reverse=True)
            
    return {
        "group_scores": group_scores,
    }