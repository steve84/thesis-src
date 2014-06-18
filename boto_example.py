# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 09:55:43 2014

@author: Steve
"""

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,FormattedContent,FreeTextAnswer,LengthConstraint,NumericConstraint,RegExConstraint
from boto.mturk.qualification import LocaleRequirement,Qualifications

title = 'Estimate the price of auction items based on title, description and images'
description = ('Take a look at an item description and estimate the corresponding price')
keywords = 'image, pricing, picture, item, estimation'

mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)

#---------------  BUILD OVERVIEW -------------------
 
overview = Overview()
overview.append(FormattedContent(html_code))
 
#---------------  BUILD QUESTION 1 -------------------
 
qc1 = QuestionContent()
qc1.append_field('Title','Price estimation (USD)')
 
qc1.append(FormattedContent(html_code))
 
fta1 = FreeTextAnswer(None, None, 1)
fta1.constraints.append(NumericConstraint(1, 1000000))          
fta1.constraints.append(RegExConstraint("^\+?([1-9]\d*).\d{0,2}$","The price has to be a positive floating point number with two digits after the point"))
 
q1 = Question(identifier="price_find",
              content=qc1,
              answer_spec=AnswerSpecification(fta1),
              is_required=True)
              
#--------------- BUILD THE QUESTION FORM -------------------
 
question_form = QuestionForm()
question_form.append(overview)
question_form.append(q1)
 
#--------------- CREATE THE HIT -------------------

qualification = Qualifications()
qualification.add(LocaleRequirement('EqualTo','US'))

hitDetails = mtc.create_hit(questions=question_form,
               max_assignments=5,
               title=title,
               description=description,
               keywords=keywords,
               duration = 60*120,
               reward=0.1,
               qualifications=qualification,
               response_groups = ['Minimal'],
               )