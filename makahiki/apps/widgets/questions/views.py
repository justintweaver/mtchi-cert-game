"""Provides the view of the widget."""
from apps.widgets.questions.models import *
import random

def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
    
    questions = []
    question_number = 0
               
    for question in random.sample(Question.objects.all(), 5):
        q = {}
        q['question'] = question.text
        q['type'] = question.type
        q['number'] = question_number
        
        question_number += 1
        
        if question.type == Question.SINGLE:            
            q['answers'] = []
            for a in Answer.objects.filter(question=question.id):
                q['answers'].append(a.answer)
        elif question.type == Question.MULTI:                       
            pass
        elif question.type == Question.MATCH:
            pass
        
        questions.append(q)
    
    print questions
        
    return {
        "questions": questions,
    }
