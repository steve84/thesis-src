# -*- coding: utf-8 -*-

import csv, os.path

def createCsvFile(file_name, resultList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel, quoting=csv.QUOTE_ALL)
        file_writer.writerow(['WorkerId'])
        for result in resultList:
            file_writer.writerow([str(result)])

def findWorkers(inputPath, inputFile):
    workerOutput = list()
    
    with open(inputPath + '/' + inputFile, 'rb') as createdHITs:
        HITreader = csv.reader(createdHITs, csv.excel)
        next(HITreader)
        for HITrow in HITreader:
            path = inputPath + '/results/HITResultsFor' + str(HITrow[1]) + '.csv'
            if os.path.isfile(path):
                with open(path, 'rb') as resultHIT:
                    Resultsreader = csv.reader(resultHIT, csv.excel, quoting=csv.QUOTE_ALL)
                    next(Resultsreader)
                    for result in Resultsreader:
                        workerOutput.append(result[4])
                        
    return workerOutput

workerIds =  findWorkers('title','createdHITs_find.csv')           
createCsvFile('../../../pure_with_commission/iteration_1/tasks/title/workerIds_find.csv', set(workerIds))

workerIds =  findWorkers('title','createdHITs_vote.csv')           
createCsvFile('../../../pure_with_commission/iteration_1/tasks/title/workerIds_vote.csv', set(workerIds))

workerIds =  findWorkers('category','createdHITs.csv')           
createCsvFile('../../../pure_with_commission/iteration_1/tasks/category/workerIds.csv', set(workerIds))

workerIds =  findWorkers('price','createdHITs.csv')           
createCsvFile('../../../pure_with_commission/iteration_1/tasks/price/workerIds.csv', set(workerIds))

workerIds =  findWorkers('evaluation','createdHITs.csv')           
createCsvFile('../../../pure_with_commission/iteration_1/tasks/evaluation/workerIds.csv', set(workerIds))