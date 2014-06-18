# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 09:55:43 2014

@author: Steve
"""

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,FormattedContent,FreeTextAnswer,LengthConstraint,NumericConstraint,RegExConstraint
from boto.mturk.qualification import LocaleRequirement,Qualifications
import csv

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
 
title = 'Estimate the price of auction items based on title, description and images (receive a commission for good work)'
description = ('Take a look at an item description and estimate the corresponding price')
keywords = 'image, pricing, picture, item, estimation, commission'

created_hits = list()
count = 1

titles = loadInputs('input_title_price.csv')
descriptions = loadInputs('input_description_price.csv')

path_groundtruth = '../../../../ground_truth/groundTruth.csv'
length = len(list(csv.reader(open(path_groundtruth, 'rb'), csv.excel_tab))) - 1

workerTable = createWorkerTable('workerIds.csv')
 
with open(path_groundtruth, 'rb') as csvfile:
    reader = csv.reader(csvfile, csv.excel_tab)
    next(reader)
    if (length == len(titles)) & (length == len(descriptions)):     
        for row in reader: 
            #---------------  BUILD OVERVIEW -------------------
             
            overview = Overview()
            
            html_code = ""
            
            html_code += 'All the workers who have done a similar task in the past are excluded from this HIT. If you find your worker ID in the following table, your work <b>will be rejected</b>.'
            html_code += '<br /><br />'        
            html_code += workerTable
            html_code += '<hr />'             
            
            html_code += '<h3><b>Title</b></h3>'
            html_code += str(titles[count-1])
            html_code += '<h3><b>Description</b></h3>'
            html_code += str(descriptions[count-1])
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
            
            overview.append(FormattedContent(html_code))
             
            #---------------  BUILD QUESTION 1 -------------------
             
            qc1 = QuestionContent()
            qc1.append_field('Title','Price estimation (USD)')
            
            html_code = ""
            html_code += 'The goal of the requester of the HIT is to generate eBay auctions by MTurk workers based on images of the item.<br />'
            html_code += 'If the auction will be sucessful then the most accurate price estimation will receive <b>0.5% of the selling price as a bonus</b>.<br /><br />'
            html_code += '<b>Instructions:</b> Estimate the price of the auction item'
            html_code += '<ul>'
            html_code += '<li>Read the item(s) description and take a look at the images (at the beginning of the HIT)</li>'
            html_code += '<li>Estimate the total price of the item(s) in USD as positive floating point number with two digits after the point (for example 50.99 or 10.00)</li>'
            html_code += '<li>You can use the internet to find prices for similar items (e.g. eBay)</li>'
            html_code += '</ul>'
            
            qc1.append(FormattedContent(html_code))
             
            fta1 = FreeTextAnswer(None, None, 1)
            fta1.constraints.append(NumericConstraint(1, 1000000))
            fta1.constraints.append(RegExConstraint("^\+?([1-9]\d*).\d{0,2}$","The price has to be a positive floating point number with two digits after the point"))
             
            q1 = Question(identifier="price_find",
                          content=qc1,
                          answer_spec=AnswerSpecification(fta1),
                          is_required=True)
                          
            #---------------  BUILD QUESTION 2 -------------------
             
            qc2 = QuestionContent()
            qc2.append_field('Title','Give reasons for your estimation')
            
            html_code = ""
            html_code += '<ul>'
            html_code += '<li>Explain your price estimation (e.g. \'Found similar item\')</li>'
            html_code += '<li>Insert valid links to webpages you used for comparing prices (e.g. completed eBay auction, www.pricegrabber.com) if possible</li>'
            html_code += '</ul>'
            html_code += '<b>Attention:</b> Only HITs with meaningful reasoning will be approved'
            
            qc2.append(FormattedContent(html_code))
            
             
            fta2 = FreeTextAnswer()
            fta2.constraints.append(LengthConstraint(20, 4000))
            fta2.constraints.append(RegExConstraint("\S","The content cannot be blank"))
             
            q2 = Question(identifier="price_find_reasons",
                          content=qc2,
                          answer_spec=AnswerSpecification(fta2),
                          is_required=True)   
                          
            #---------------  BUILD QUESTION 3 -------------------
             
            qc3 = QuestionContent()
            qc3.append_field('Title','Additional information (optional)')
            
            html_code = ""
            html_code += 'If you can\'t estimate a price for the auction item(s) then tell us which additional information do you need.'
            qc3.append(FormattedContent(html_code))
             
            fta3 = FreeTextAnswer()
             
            q3 = Question(identifier="price_find_missing_information",
                          content=qc3,
                          answer_spec=AnswerSpecification(fta3)) 
                          
            #---------------  BUILD QUESTION 4 -------------------
             
            qc4 = QuestionContent()
            qc4.append_field('Title','Your personal feedback (optional)')
            
            html_code = ""
            html_code += 'Give your personal feedback about the task. This <b>can</b> contain one of the following aspects:'
            html_code += '<ul>'
            html_code += '<li>Problems of the task (e.g. images do not contain an item)</li>'
            html_code += '<li>Instructions are not clear enough</li>'
            html_code += '</ul>'
            qc4.append(FormattedContent(html_code))
             
            fta4 = FreeTextAnswer()
             
            q4 = Question(identifier="price_find_feedback",
                          content=qc4,
                          answer_spec=AnswerSpecification(fta4))  
                          
            #--------------- BUILD THE QUESTION FORM -------------------
             
            question_form = QuestionForm()
            question_form.append(overview)
            question_form.append(q1)
            question_form.append(q2)
            question_form.append(q3)
            question_form.append(q4)
             
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
    
            created_hits.append([count, hitDetails[0].HITId])
            count += 1
            
        createCsvFile('createdHITs.csv', created_hits)                       
