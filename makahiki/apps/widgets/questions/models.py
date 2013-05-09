from django.db import models
from django.db.models.fields.related import ForeignKey


class Question(models.Model):
    """Question model"""
    SINGLE = 'SINGLE'
    MULTI = 'MULTI'
    MATCH = 'MATCH'
    QUESTION_TYPE_CHOICES = (
        (SINGLE, 'Single Correct Answer'),
        (MULTI, 'Multiple Correct Answers'),
        (MATCH, 'Matching'),
    )
    
    type = models.CharField(max_length = 8,
                            choices = QUESTION_TYPE_CHOICES,
                            default = SINGLE)
    
    text = models.CharField(max_length = 1023)
    
    
class Answer(models.Model):
    """Answer model"""
    question = models.ForeignKey('Question')
    
    answer = models.CharField(max_length = 1023)
    
    
class CorrectSingleAnswer(models.Model):
    """CorrectSingleAnswer model"""
    question = models.ForeignKey('Question',
                                 unique = True)
    
    answer = models.ForeignKey('Answer')
    
    
class CorrectMultipleAnswers(models.Model):
    """CorrectMultipleAnswers model"""
    question = models.ForeignKey('Question')
    
    answer = models.ForeignKey('Answer')
    
    
class MatchingChoices(models.Model):
    """MatchingChoices model"""
    question = models.ForeignKey('Question')
    
    given = models.CharField(max_length = 1023)
    
    match = models.CharField(max_length = 1023)
    
    
    