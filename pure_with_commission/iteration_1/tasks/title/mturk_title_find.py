# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 09:55:43 2014

@author: Steve
"""

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,FormattedContent,FreeTextAnswer,LengthConstraint,RegExConstraint
from boto.mturk.qualification import LocaleRequirement,Qualifications
import csv


def createCsvFile(file_name, hitList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel)
        file_writer.writerow(['Ground truth number','HITId'])
        for hit in hitList:
            file_writer.writerow([str(hit[0]), str(hit[1])])
            
def createWorkerTable(workerFile):
    htmlWorkerTable = ""
    htmlWorkerTable += '<table border= \"1\">'
    htmlWorkerTable += '<tr><td><b>Worker ID</b></td></tr>'
    with open(workerFile, 'rb') as csvfile:
        reader = csv.reader(csvfile, csv.excel_tab)
        next(reader)
        for row in reader:
            htmlWorkerTable += '<tr><td>' + str(row[0]) + '</td></tr>'
            
    htmlWorkerTable += '</table>'
    return htmlWorkerTable

ACCESS_ID = ''
SECRET_KEY = ''
HOST = ''

keys = open('../../keys.csv','rb')
file_reader = csv.reader(keys)
for row in file_reader:
    ACCESS_ID = str(row[0])
    SECRET_KEY = str(row[1])
    HOST = str(row[2])
    
mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)
 
title = 'Give auction items a title based on several images (receive a commission for good work)'
description = ('Take a look at three pictures of an auction item and write down a predicative title.')
keywords = 'image, description, picture, item, title, auction, commission'

created_hits = list()
count = 1

workerTable = createWorkerTable('workerIds_find.csv')

with open('../../../../ground_truth/groundTruth.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, csv.excel_tab)
    next(reader)
    for row in reader:
        #---------------  BUILD OVERVIEW -------------------
        overview = Overview()
        
        html_code = ""
        html_code += 'All the workers who have done a similar task in the past are excluded from this HIT. If you find your worker ID in the following table, your work <b>will be rejected</b>.'
        html_code += '<br /><br />'        
        html_code += workerTable
        html_code += '<hr />'
        html_code += '<h1>Make a clear, compelling first impression by writing a great title for the auction item(s) on the pictures</h1>'
        html_code += '<table><tr>'
        html_code += '<td><img src="' + str(row[5]) + '" alt="Image 1" width="250" border="2"></img></td>'
        html_code += '<td><img src="' + str(row[6]) + '" alt="Image 2" width="250" border="2"></img></td>'
        html_code += '<td><img src="' + str(row[7]) + '" alt="Image 3" width="250" border="2"></img></td>'
        html_code += '</tr>'
        html_code += '<tr>'
        html_code += '<td><a href="' + str(row[5]) + '" target="_blank">Link to full size image 1 (new window)</a></td>'
        html_code += '<td><a href="' + str(row[6]) + '" target="_blank">Link to full size image 2 (new window)</a></td>'
        html_code += '<td><a href="' + str(row[7]) + '" target="_blank">Link to full size image 3 (new window)</a></td>'        
        html_code += '</tr></table>'
        
        overview.append(FormattedContent(html_code))
         
        #---------------  BUILD QUESTION 1 -------------------
         
        qc1 = QuestionContent()
        qc1.append_field('Title','Auction item title')
        
        html_code = ""
        html_code += 'The goal of the requester of the HIT is to generate eBay auctions by MTurk workers based on images of the item.<br />'
        html_code += 'If the auction will be sucessful then the creator of the final title will receive <b>0.25% of the selling price as a bonus</b>. The final title will be determined by a voting procedure.'
        html_code += '<table cellspacing="5">'
        html_code += '<tr><td><b>Instructions:</b></td></tr>'
        html_code += '<tr><td>Write a title which describes the item(s) on the pictures, inside the empty text field below and keep in mind the following remarks:</td><td>Example</td></tr>'
        html_code += '<tr><td><ul>'
        html_code += '<li>Use descriptive keywords to clearly and accurately convey what you\'re seeing. You\'re allowed <b>up to 80 characters</b>, but you don\'t need to use them all</li>'
        html_code += '<li>Include the item\'s brand name, artist, or designer if possible</li>'
        html_code += '<li>Include item specifics. For example, include size, color, condition, and model number if possible</li>'
        html_code += '<li>Use correct spelling</li>'
        html_code += '<li>Don\'t use all caps</li>'
        html_code += '<li>Take a look at the provided example</li>'
        html_code += '</ul></td><td><img src="http://ecx.images-amazon.com/images/I/61aeYFqV3IL._SL1425_.jpg" alt="Example" width="250" border="2"></img></td></tr>'
        html_code += '<tr><td></td><td>Title: Sony Playstation 4 (black), 1 Controller, New</td></tr>'
        html_code += '</table>'
        
        qc1.append(FormattedContent(html_code))
         
        fta1 = FreeTextAnswer(None, None, 1)
        fta1.constraints.append(LengthConstraint(None, 80))
        fta1.constraints.append(RegExConstraint("\S","The content cannot be blank"))
         
        q1 = Question(identifier="title_find",
                      content=qc1,
                      answer_spec=AnswerSpecification(fta1),
                      is_required=True)
                      
        #---------------  BUILD QUESTION 2 -------------------
         
        qc2 = QuestionContent()
        qc2.append_field('Title','Your personal feedback (optional)')
        
        html_code = ""
        html_code += 'Give your personal feedback about the task. This <b>can</b> contain one of the following aspects:'
        html_code += '<ul>'
        html_code += '<li>Problems of the task (e.g. images are not visible)</li>'
        html_code += '<li>Instructions are not clear enough</li>'
        html_code += '<li>Example was not helpful</li>'
        html_code += '</ul>'
        qc2.append(FormattedContent(html_code))
         
        fta2 = FreeTextAnswer()
         
        q2 = Question(identifier="title_find_feedback",
                      content=qc2,
                      answer_spec=AnswerSpecification(fta2))
         
        #--------------- BUILD THE QUESTION FORM -------------------
         
        question_form = QuestionForm()
        question_form.append(overview)
        question_form.append(q1)
        question_form.append(q2)
         
        #--------------- CREATE THE HIT -------------------
         
        qualification = Qualifications()
        qualification.add(LocaleRequirement('EqualTo','US'))  
        
        hitDetails = mtc.create_hit(questions=question_form,
                       max_assignments=3,
                       title=title,
                       description=description,
                       keywords=keywords,
                       duration = 60*30,
                       reward=0.05,
                       qualifications=qualification,
                       response_groups = ['Minimal'],
                       )
                       
        created_hits.append([count, hitDetails[0].HITId])
        count += 1
        
createCsvFile('createdHITs_find.csv', created_hits)