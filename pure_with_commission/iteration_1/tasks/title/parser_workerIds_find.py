# -*- coding: utf-8 -*-

import csv, os.path

def createCsvFile(file_name, resultList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel, quoting=csv.QUOTE_ALL)
        file_writer.writerow(['WorkerId'])
        for result in resultList:
            file_writer.writerow([str(result)])

def findWorkers(inputFile):
    workerOutput = list()
    
    with open(inputFile, 'rb') as createdHITs:
        HITreader = csv.reader(createdHITs, csv.excel)
        next(HITreader)
        for HITrow in HITreader:
            path = 'results/HITResultsFor' + str(HITrow[1]) + '.csv'
            if os.path.isfile(path):
                with open(path, 'rb') as resultHIT:
                    Resultsreader = csv.reader(resultHIT, csv.excel, quoting=csv.QUOTE_ALL)
                    next(Resultsreader)
                    for result in Resultsreader:
                        workerOutput.append(result[4])
                        
    return workerOutput

workerIds =  findWorkers('createdHITs_find.csv')           
createCsvFile('workerIds_find_vote_commission.csv', set(workerIds))