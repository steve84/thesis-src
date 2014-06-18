# -*- coding: utf-8 -*-

import csv, os.path, dateutil.parser
from pytz import timezone
from boto.mturk.connection import MTurkConnection

def createCsvFile(file_name, resultList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel, quoting=csv.QUOTE_ALL)
        file_writer.writerow(['Ground truth number','Category','Average working time (s)','Average finishing time (s)','Average reaction time (s)'])
        for result in resultList:
            if len(result) == 5:
                file_writer.writerow([str(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4])])
                
def createDatFile(file_name, resultList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel_tab, quoting=csv.QUOTE_NONE)
        file_writer.writerow(['#Ground truth number','Average working time (s)','Average finishing time (s)','Average reaction time (s)'])
        for result in resultList:
            if len(result) == 5:
                file_writer.writerow([str(result[0]), str(result[2]), str(result[3]), str(result[4])])                
                
def majorityVoting(categories):
    category_list = list()
    for category in categories:
        isInList = False
        for item in category_list:
            if str(category) in item:
                item[0] += 1
                isInList = True
        if not isInList:
            category_list.append([1,str(category)])
    
    majority = int(len(categories) / 2) + 1
    category_list.sort(reverse=True)
    
    if category_list[0][0] >= majority:
        return str(category_list[0][1])
    else:
        return 'None'  
        
def avgTime(startTimes, endTimes):
    timeCount = float(0)
    for x in range(0, len(startTimes)):
        startTime = dateutil.parser.parse(str(startTimes[x]))
        endTime = dateutil.parser.parse(str(endTimes[x]))
        timeCount += (endTime - startTime).seconds
    return float(timeCount / len(startTimes))

def convertUTCtoPDT(utc_dt):
    utc_dt = dateutil.parser.parse(str(utc_dt))
    pac_tz = timezone('US/Pacific')
    pdt_dt = pac_tz.normalize(utc_dt.astimezone(pac_tz))
    pdt_dt = pdt_dt.replace(tzinfo=None)
    return str(pdt_dt)    
    
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

categoryOutput = list()

with open('createdHITs.csv', 'rb') as createdHITs:
    HITreader = csv.reader(createdHITs, csv.excel)
    next(HITreader)
    for HITrow in HITreader:
        path = 'results/HITResultsFor' + str(HITrow[1]) + '.csv'
        if os.path.isfile(path):
            categories = list()
            acceptTimes = list()
            submitTimes = list()
            creationTimes = list()            
            with open(path, 'rb') as resultHIT:
                Resultsreader = csv.reader(resultHIT, csv.excel, quoting=csv.QUOTE_ALL)
                next(Resultsreader)
                for result in Resultsreader:
                    if str(result[5]).find('Approved') >= 0:
                        categories.append(result[8])
                        acceptTimes.append(result[6])
                        submitTimes.append(result[7])
                        hit = mtc.get_hit(str(result[0]))
                        creationTimes.append(convertUTCtoPDT(str(hit[0].CreationTime)))                        
            categoryOutput.append([str(HITrow[0]),str(majorityVoting(categories)), str(avgTime(acceptTimes, submitTimes)), str(avgTime(creationTimes, submitTimes)), str(avgTime(creationTimes, acceptTimes))])
            
createCsvFile('../../output/output_category.csv', categoryOutput)
createCsvFile('../evaluation/input_category_evaluation.csv', categoryOutput)
createDatFile('../../output/dat/output_category.dat', categoryOutput)