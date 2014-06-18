# -*- coding: utf-8 -*-

import csv, os.path, dateutil.parser
from pytz import timezone
from boto.mturk.connection import MTurkConnection

def createCsvFile(file_name, resultList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel, quoting=csv.QUOTE_ALL)
        file_writer.writerow(['Ground truth number','Evaluation','Votes of crowdsourced content with commission (in %)','Average working time (s)','Average finishing time (s)','Average reaction time (s)'])
        for result in resultList:
            if len(result) == 5:
                file_writer.writerow([str(result[0]), str(result[1][0]), str(result[1][1]), str(result[2]), str(result[3]), str(result[4])])
                
def createDatFile(file_name, resultList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel_tab, quoting=csv.QUOTE_NONE)
        file_writer.writerow(['#Ground truth number','Votes of crowdsourced content with commission (in %)','Average working time (s)','Average finishing time (s)','Average reaction time (s)'])
        for result in resultList:
            if len(result) == 5:
                file_writer.writerow([str(result[0]), str(result[1][1]), str(result[2]), str(result[3]), str(result[4])])                
                
def majorityVoting(votes, crowdsourced_option):
    vote_list = list()
    for vote in votes:
        isInList = False
        for item in vote_list:
            if str(vote) in item:
                item[0] += 1
                isInList = True
        if not isInList:
            vote_list.append([1,str(vote)])
    
    majority = int(len(votes) / 2) + 1
    vote_list.sort(reverse=True)
    
    if vote_list[0][0] >= majority:
        if str(vote_list[0][1]) == str(crowdsourced_option):
            return ['Pure crowdsourced content (with commission)',float(float(vote_list[0][0]) / len(votes))]
        else:
            if len(vote_list) > 1:
                return ['Ground truth',float(float(vote_list[1][0]) / len(votes))]
            else:
                return ['Ground truth',float(0)]
    else:
        return 'None'
        
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

titles = loadInputs('input_title_evaluation.csv')
evaluationOutput = list()

with open('createdHITs_commission.csv', 'rb') as createdHITs:
    HITreader = csv.reader(createdHITs, csv.excel)
    next(HITreader)
    x = 0
    for HITrow in HITreader:
        path = 'results/HITResultsFor' + str(HITrow[1]) + '.csv'
        if os.path.isfile(path):
            results = list()
            acceptTimes = list()
            submitTimes = list()
            creationTimes = list()            
            with open(path, 'rb') as resultHIT:
                Resultsreader = csv.reader(resultHIT, csv.excel, quoting=csv.QUOTE_ALL)
                next(Resultsreader)
                for result in Resultsreader:
                    if str(result[5]).find('Approved') >= 0:                    
                        results.append(result[8])
                        acceptTimes.append(result[6])
                        submitTimes.append(result[7])
                        hit = mtc.get_hit(str(result[0]))
                        creationTimes.append(convertUTCtoPDT(str(hit[0].CreationTime)))                        
            evaluationOutput.append([str(HITrow[0]),majorityVoting(results, titles[x]), str(avgTime(acceptTimes, submitTimes)), str(avgTime(creationTimes, submitTimes)), str(avgTime(creationTimes, acceptTimes))])
            x += 1

          
createCsvFile('../../output/output_pure_vs_commission_evaluation.csv', evaluationOutput)
createDatFile('../../output/dat/output_pure_vs_commission_evaluation.dat', evaluationOutput)
