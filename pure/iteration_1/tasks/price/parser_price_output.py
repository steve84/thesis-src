# -*- coding: utf-8 -*-

import csv, os.path, dateutil.parser
from pytz import timezone
from boto.mturk.connection import MTurkConnection

def createCsvFile(file_name, resultList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel, quoting=csv.QUOTE_ALL)
        file_writer.writerow(['Ground truth number','Price','Average working time (s)','Average finishing time (s)','Average reaction time (s)','Root Mean Squared Error (Price)','Ground truth price'])
        for result in resultList:
            if len(result) == 7:
                file_writer.writerow([str(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]), str(result[5]), str(result[6])])

def createDatFile(file_name, resultList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel_tab, quoting=csv.QUOTE_NONE)
        file_writer.writerow(['#Ground truth number','Price','Average working time (s)','Average finishing time (s)','Average reaction time (s)','Root Mean Squared Error (Price)','Ground truth price'])
        for result in resultList:
            if len(result) == 7:
                file_writer.writerow([str(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]), str(result[5]), str(result[6])]) 
                
def averagePrice(prices):
    sumPrices = 0
    nbrPrices = 0
    for price in prices:
        sumPrices += float(price)
        nbrPrices += 1
        
    return (sumPrices / nbrPrices)
        
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
    
def RMSError(values, ground_truth):
    rmse = 0
    for value in values:
        rmse += pow((value - ground_truth), 2)
    rmse = (rmse / len(values))
    return pow(rmse, 0.5)
    
def loadPrices():
    path_groundtruth = '../../../../ground_truth/groundTruth.csv'
    prices = list()
    with open(path_groundtruth, 'rb') as csvfile:
        reader = csv.reader(csvfile, csv.excel_tab)
        next(reader)
        for row in reader:
            prices.append(float(row[4]))
            
    return prices

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

priceOutput = list()
priceList = loadPrices()

with open('createdHITs.csv', 'rb') as createdHITs:
    HITreader = csv.reader(createdHITs, csv.excel)
    next(HITreader)
    cnt = 0
    for HITrow in HITreader:
        path = 'results/HITResultsFor' + str(HITrow[1]) + '.csv'
        if os.path.isfile(path):
            prices = list()
            acceptTimes = list()
            submitTimes = list()
            creationTimes = list()            
            with open(path, 'rb') as resultHIT:
                Resultsreader = csv.reader(resultHIT, csv.excel, quoting=csv.QUOTE_ALL)
                next(Resultsreader)
                for result in Resultsreader:
                    if str(result[5]).find('Approved') >= 0:                    
                        prices.append(float(result[8]))
                        acceptTimes.append(result[6])
                        submitTimes.append(result[7])
                        hit = mtc.get_hit(str(result[0]))
                        creationTimes.append(convertUTCtoPDT(str(hit[0].CreationTime)))                        
            priceOutput.append([str(HITrow[0]),str(averagePrice(prices)), str(avgTime(acceptTimes, submitTimes)), str(avgTime(creationTimes, submitTimes)), str(avgTime(creationTimes, acceptTimes)), str(RMSError(prices, priceList[cnt])), str(priceList[cnt])])
            cnt += 1

createCsvFile('../../output/output_price.csv', priceOutput)
createDatFile('../../output/dat/output_price.dat', priceOutput)