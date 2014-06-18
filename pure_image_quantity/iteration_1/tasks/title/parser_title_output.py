# -*- coding: utf-8 -*-

import csv, os.path, dateutil.parser
from pytz import timezone
from boto.mturk.connection import MTurkConnection

def createCsvFile(file_name, resultList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel, quoting=csv.QUOTE_ALL)
        file_writer.writerow(['Ground truth number','Title','Average finding working time (s)','Average finding finishing time (s)','Average finding reaction time (s)','Average voting working time (s)','Average voting finishing time (s)','Average voting reaction time (s)','Length of title'])
        for result in resultList:
            if len(result) == 9:
                file_writer.writerow([str(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]), str(result[5]), str(result[6]), str(result[7]), str(result[8])])

def createDatFile(file_name, resultList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel_tab, quoting=csv.QUOTE_NONE)
        file_writer.writerow(['#Ground truth number','Title','Average finding working time (s)','Average finding finishing time (s)','Average finding reaction time (s)','Average voting working time (s)','Average voting finishing time (s)','Average voting reaction time (s)','Length of title'])
        for result in resultList:
            if len(result) == 9:
                file_writer.writerow([str(result[0]), str(result[2]), str(result[3]), str(result[4]), str(result[5]), str(result[6]), str(result[7]), str(result[8])])                  
                
def majorityVoting(votes):
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
        return str(vote_list[0][1])
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

titleOutput = list()
findTitleWorkingTimes = list()
findTitleFinishingTimes = list()
findTitleReactionTimes = list()

with open('createdHITs_find.csv', 'rb') as createdHITs:
    HITreader = csv.reader(createdHITs, csv.excel)
    next(HITreader)
    for HITrow in HITreader:
        path = 'results/HITResultsFor' + str(HITrow[1]) + '.csv'
        if os.path.isfile(path):
            acceptTimes = list()
            submitTimes = list()
            creationTimes = list()
            with open(path, 'rb') as resultHIT:
                Resultsreader = csv.reader(resultHIT, csv.excel, quoting=csv.QUOTE_ALL)
                next(Resultsreader)
                for result in Resultsreader:
                    if str(result[5]).find('Approved') >= 0:
                        acceptTimes.append(result[6])
                        submitTimes.append(result[7])
                        hit = mtc.get_hit(str(result[0]))
                        creationTimes.append(convertUTCtoPDT(str(hit[0].CreationTime)))
            findTitleWorkingTimes.append(str(avgTime(acceptTimes, submitTimes)))
            findTitleFinishingTimes.append(str(avgTime(creationTimes, submitTimes)))
            findTitleReactionTimes.append(str(avgTime(creationTimes, acceptTimes)))

with open('createdHITs_vote.csv', 'rb') as createdHITs:
    HITreader = csv.reader(createdHITs, csv.excel)
    count = 0
    next(HITreader)
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
            title = str(majorityVoting(results))
            titleOutput.append([str(HITrow[0]), title, str(findTitleWorkingTimes[count]), str(findTitleFinishingTimes[count]), str(findTitleReactionTimes[count]), str(avgTime(acceptTimes, submitTimes)), str(avgTime(creationTimes, submitTimes)), str(avgTime(creationTimes, acceptTimes)), str(len(title))])
            count += 1

titleOutput.reverse()
createCsvFile('../category/input_category_find.csv', titleOutput)
createCsvFile('../price/input_title_price.csv', titleOutput)
createCsvFile('../evaluation/input_title_evaluation.csv', titleOutput)
createCsvFile('../../output/output_title.csv', titleOutput)
createDatFile('../../output/dat/output_title.dat', titleOutput)