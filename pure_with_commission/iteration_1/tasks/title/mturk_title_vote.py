# -*- coding: utf-8 -*-
"""
Created on Mon Mar 03 17:51:37 2014

@author: Steve
"""

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,FormattedContent,SelectionAnswer,FreeTextAnswer,LengthConstraint,RegExConstraint
from boto.mturk.qualification import LocaleRequirement,Qualifications
import csv, random

def loadTitles(csv_file_name):
    with open(csv_file_name, 'rb') as csv_file:
        HITlist = list()
        file_reader = csv.reader(csv_file, csv.excel)
        file_reader.next()
        for row in file_reader:
            titles = list()
            for x in random.sample(range(1,len(row)),len(row)-1):
                cat = str(row[x])
                cat = cat.replace('&', '&amp;')
                titleTuple = cat, cat
                titles.append(titleTuple)
                
            titles.append(('None','None'))    
            HITlist.append(titles)
        return HITlist
        
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
 
title = 'Vote for an auction item title based on several images (receive a commission for good work)'
description = ('Take a look at three pictures of an auction item and select a title')
keywords = 'image, description, picture, item, title, vote, auction, commission'

created_hits = list()
count = 1

ratings = loadTitles('input_title_vote.csv')
workerTable = createWorkerTable('workerIds_vote.csv')

path_groundtruth = '../../../../ground_truth/groundTruth.csv'
length = len(list(csv.reader(open(path_groundtruth, 'rb'), csv.excel_tab))) - 1


with open(path_groundtruth, 'rb') as csvfile:
    reader = csv.reader(csvfile, csv.excel_tab)
    next(reader)
    if length == len(ratings):
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
            qc1.append_field('Title','Voting for an auction item title')
            
            html_code = ""
            html_code += 'The goal of the requester of the HIT is to generate eBay auctions by MTurk workers based on images of the item.<br />'
            html_code += 'If the auction will be sucessful then the voters, who voted for the final title, will receive <b>0.1% of the selling price as a bonus</b>.<br /><br />'            
            html_code += '<b>Instructions:</b> Select the title which describes clearly and accurately the auction item(s) on the pictures. Keep in mind the following restrictions:'
            html_code += '<ul>'
            html_code += '<li>Do <b>not select</b> a title which contains <b>wrong information</b></li>'
            html_code += '<li>Do <b>not select</b> a title which has <b>spelling mistakes</b> (e.g. Sny Playstation 4, black)</li>'
            html_code += '<li>Do <b>not select</b> a title which is written in <b>capital letters</b> (e.g. SONY PLAYSTATION 4, BLACK)</li>'
            html_code += '</ul>'
            html_code += 'If you think that no title is suitable for the item(s) then select None'
            
            qc1.append(FormattedContent(html_code))
            
            fta1 = SelectionAnswer(min=1, max=1,style='radiobutton',
                                  selections=ratings[count-1],
                                  type='text',
                                  other=False)
             
            q1 = Question(identifier='title_vote',
                          content=qc1,
                          answer_spec=AnswerSpecification(fta1),
                          is_required=True)
                          
            #---------------  BUILD QUESTION 2 -------------------
             
            qc2 = QuestionContent()
            qc2.append_field('Title','Give reasons for your selection')
            
            html_code = ""
            html_code += '<ul>'
            html_code += '<li>Explain why the selected title is the best description of the item(s) on the pictures</li>'
            html_code += '<li>Explain the deficits of the non-selected titles (e.g. incorrect information)</li>'
            html_code += '</ul>'
            html_code += '<b>Attention:</b> Only HITs with meaningful reasoning will be approved'
            
            qc2.append(FormattedContent(html_code))
            
             
            fta2 = FreeTextAnswer()
            fta2.constraints.append(LengthConstraint(20, 4000))
            fta2.constraints.append(RegExConstraint("\S","The content cannot be blank"))
             
            q2 = Question(identifier="title_vote_reasons",
                          content=qc2,
                          answer_spec=AnswerSpecification(fta2),
                          is_required=True)              
            
            #---------------  BUILD QUESTION 3 -------------------
             
            qc3 = QuestionContent()
            qc3.append_field('Title','Your personal feedback (optional)')
            
            html_code = ""
            html_code += 'Give your personal feedback about the task. This <b>can</b> contain one of the following aspects:'
            html_code += '<ul>'
            html_code += '<li>Problems of the task (e.g. images do not contain an item)</li>'
            html_code += '<li>Instructions are not clear enough</li>'
            html_code += '</ul>'
            qc3.append(FormattedContent(html_code))
             
            fta3 = FreeTextAnswer()
             
            q3 = Question(identifier="title_vote_feedback",
                          content=qc3,
                          answer_spec=AnswerSpecification(fta3))  
                          
            #--------------- BUILD THE QUESTION FORM -------------------
             
            question_form = QuestionForm()
            question_form.append(overview)
            question_form.append(q1)
            question_form.append(q2)
            question_form.append(q3)
             
            #--------------- CREATE THE HIT -------------------
             
            qualification = Qualifications()
            qualification.add(LocaleRequirement('EqualTo','US'))   
             
            hitDetails = mtc.create_hit(questions=question_form,
                           max_assignments=3,
                           title=title,
                           description=description,
                           keywords=keywords,
                           duration = 60*30,
                           reward=0.02,
                           qualifications=qualification,
                           response_groups = ['Minimal'],
                           )
                           
            created_hits.append([count, hitDetails[0].HITId])
            count += 1
        
        createCsvFile('createdHITs_vote.csv', created_hits)