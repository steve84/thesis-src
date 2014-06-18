# -*- coding: utf-8 -*-
"""
Created on Mon Mar 03 17:51:37 2014

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
            
def loadTitles(csv_file_name):
    with open(csv_file_name, 'rb') as csv_file:
        titles = list()
        file_reader = csv.reader(csv_file, csv.excel)
        file_reader.next()
        for row in file_reader:
            titles.append(str(row[1]).replace('&','&amp;'))
        return titles

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

title = 'Find a category of an auction item based on several images' 
description = ('Take a look at three pictures of an auction item and find a category')
keywords = 'image, categorization, picture, item, category'

created_hits = list()
count = 1

titles = loadTitles('input_category_find.csv')

path_groundtruth = '../../../../ground_truth/groundTruth.csv'
length = len(list(csv.reader(open(path_groundtruth, 'rb'), csv.excel_tab))) - 1

with open(path_groundtruth, 'rb') as csvfile:
    reader = csv.reader(csvfile, csv.excel_tab)
    next(reader)
    if length == len(titles):    
        for row in reader: 
            #---------------  BUILD OVERVIEW -------------------
             
            overview = Overview()
            
            html_code = ""
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
            qc1.append_field('Title','Find a category for auction items')
            
            html_code = ""
            html_code += 'The goal of the requester of the HIT is to generate eBay auctions by MTurk workers based on images of the item<br /><br />'
            html_code += '<b>Instructions:</b> Find a category which matches best for the auction item(s) on the pictures'
            html_code += '<ol>'
            html_code += '<li>Click on the link: <a href="http://www.ebay.com" target="_blank">http://www.ebay.com</a></li>'
            html_code += '<li>Copy the text <b>"' + str(titles[count-1]) + '"</b> into the search field on top of the website</li>'
            html_code += '<li>Press the \'Search\' button</li>'
            html_code += '<li>Insert the most suitable category into the text field below the instructions (Example: Video Games &amp; Consoles for the text \'Playstation 4\'). <i>Hint:</i> Categories will be displayed on the left side under the eBay logo</li>'
            html_code += '<li>If no categories are displayed then the title is too specific. Try to remove unnecessary keywords until a category is displayed. For example: The title "Yogi Berra TOPPS Baseball Card #425, New York Yankees, Catcher-Outfield" will not display a category, but "Yogi Berra TOPPS Baseball Card" will</li>'
            html_code += '</ol>'
            
            qc1.append(FormattedContent(html_code))
            
            fta1 = FreeTextAnswer(None, None, 1)
            fta1.constraints.append(LengthConstraint(None, 80))
            fta1.constraints.append(RegExConstraint("\S","The content cannot be blank"))
             
            q1 = Question(identifier="category_find",
                          content=qc1,
                          answer_spec=AnswerSpecification(fta1),
                          is_required=True)
                          
            #---------------  BUILD QUESTION 2 -------------------
             
            qc2 = QuestionContent()
            qc2.append_field('Title','Your personal feedback (optional)')
            
            html_code = ""
            html_code += 'Give your personal feedback about the task. This <b>can</b> contain one of the following aspects:'
            html_code += '<ul>'
            html_code += '<li>Problems of the task (e.g. images do not contain an item)</li>'
            html_code += '<li>Instructions are not clear enough</li>'
            html_code += '<li>Example was not helpful</li>'
            html_code += '</ul>'
            qc2.append(FormattedContent(html_code))
             
            fta2 = FreeTextAnswer()
            
            q2 = Question(identifier="category_find_feedback",
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
            
        createCsvFile('createdHITs.csv', created_hits)