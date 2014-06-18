# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 09:55:43 2014

@author: Steve
"""

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,FormattedContent,SelectionAnswer,FreeTextAnswer,LengthConstraint,RegExConstraint
from boto.mturk.qualification import LocaleRequirement,Qualifications
import csv, random

def createCsvFile(file_name, hitList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel)
        file_writer.writerow(['Ground truth number','HITId'])
        for hit in hitList:
            file_writer.writerow([str(hit[0]), str(hit[1])])
            
def loadInputs(csv_file_name):
    with open(csv_file_name, 'rb') as csv_file:
        inputs = list()
        file_reader = csv.reader(csv_file, csv.excel)
        file_reader.next()
        for row in file_reader:
            input = str(row[1])
            input = input.replace('&','&amp;')
            inputs.append(input)
        return inputs                   
 
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
 
title = 'Choose between two auction item descriptions'
description = ('Take a look at two auction item descriptions and select the best one')
keywords = 'image, pricing, picture, item, description, title, voting, auction'

created_hits = list()
count = 1

titles = loadInputs('input_title_evaluation.csv')
descriptions = loadInputs('input_description_evaluation.csv')
categories = loadInputs('input_category_evaluation.csv')

path_groundtruth = '../../item/groundTruth.csv'
length = len(list(csv.reader(open(path_groundtruth, 'rb'), csv.excel_tab))) - 1
 
with open(path_groundtruth, 'rb') as csvfile:
    reader = csv.reader(csvfile, csv.excel_tab)
    next(reader)
    if (length == len(titles)) & (length == len(descriptions)) & (length == len(categories)):     
        for row in reader:
            #---------------  BUILD OVERVIEW -------------------
            crowdsourced_content = [str(titles[count-1]), str(descriptions[count-1]), str(categories[count-1])]
            ground_truth = [str(row[0]).replace('&','&amp;'), str(row[1]).replace('&','&amp;'), str(row[2]).replace('&','&amp;')]          
            options = [crowdsourced_content, ground_truth]
            rnd = random.sample(range(0,2),2)
             
            overview = Overview()
            
            html_code = ""
            html_code += '<h3><b>Images</b></h3>'
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
            html_code += '<hr />'
            html_code += '<h3><b>Descriptions</b></h3>'
            html_code += '<table border="1" frame="void" cellspacing="5">'
            html_code += '<tr><td></td><td width="50%"><b>Option A</b></td><td width="50%"><b>Option B</b></td></tr>'
            html_code += '<tr><td><b>Title</b></td><td>' + options[rnd[0]][0] + '</td><td>' + options[rnd[1]][0] + '</td></tr>'
            html_code += '<tr><td><b>Description</b></td><td>' + options[rnd[0]][1] + '</td><td>' + options[rnd[1]][1] + '</td></tr>'
            html_code += '<tr><td><b>Category</b></td><td>' + options[rnd[0]][2] + '</td><td>' + options[rnd[1]][2] + '</td></tr>'
            html_code += '</table>'
            
            overview.append(FormattedContent(html_code))
             
            #---------------  BUILD QUESTION 1 -------------------
             
            qc1 = QuestionContent()
            qc1.append_field('Title','Select better description')
            
            html_code = ""
            html_code += '<b>Instructions:</b> Select the better description of the auction item'
            html_code += '<ul>'
            html_code += '<li>Read the descriptions of option A and B and take a look at the item(s) on the images (at the beginning of the HIT)</li>'
            html_code += '<li>Select the option (A or B) which provides a clear and accurate description of the auction item(s)</li>'
            html_code += '</ul>'
            
            qc1.append(FormattedContent(html_code))
            
            ratings = [('Option A', options[rnd[0]][0]),('Option B', options[rnd[1]][0])]
             
            fta1 = SelectionAnswer(min=1, max=1,style='radiobutton',
                                  selections=ratings,
                                  type='text',
                                  other=False)
             
            q1 = Question(identifier='evaluation',
                          content=qc1,
                          answer_spec=AnswerSpecification(fta1),
                          is_required=True)
                          
            #---------------  BUILD QUESTION 2 -------------------
             
            qc2 = QuestionContent()
            qc2.append_field('Title','Give reasons for your selection')
            
            html_code = ""
            html_code += '<ul>'
            html_code += '<li>Explain why the selected option is the better description of the auction item(s) on the pictures</li>'
            html_code += '<li>Explain the deficits of the non-selected option (e.g. missing or incorrect information)</li>'
            html_code += '</ul>'
            html_code += '<b>Attention:</b> Only HITs with meaningful reasoning will be approved'
            
            qc2.append(FormattedContent(html_code))
            
             
            fta2 = FreeTextAnswer()
            fta2.constraints.append(LengthConstraint(20, 4000))
            fta2.constraints.append(RegExConstraint("\S","The content cannot be blank"))
             
            q2 = Question(identifier="evaluation_reasons",
                          content=qc2,
                          answer_spec=AnswerSpecification(fta2))   
                          
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
             
            q3 = Question(identifier="evaluation_feedback",
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
                           max_assignments=5,
                           title=title,
                           description=description,
                           keywords=keywords,
                           duration = 60*60,
                           reward=0.1,
                           qualifications=qualification,
                           response_groups = ['Minimal'],
                           )
                  
            created_hits.append([count, hitDetails[0].HITId])
            count += 1
            
        createCsvFile('createdHITs.csv', created_hits)              