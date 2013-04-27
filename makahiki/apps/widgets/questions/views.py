"""Provides the view of the widget."""
from apps.widgets.questions.models import *

def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    
    questions = []
    
    for question in Question.objects.all():
        q = {}
        q['question'] = question.text
        q['type'] = question.type
        
        if question.type == Question.SINGLE:
            pass
        elif question.type == Question.MULTI:
            pass
        elif question.type == Question.MATCH:
            pass
        
        questions.append(q)
    
    print questions
        
    return {
        "questions": questions,
    }
