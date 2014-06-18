# -*- coding: utf-8 -*-

import csv, os.path

def createCsvFile(file_name, resultList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel, quoting=csv.QUOTE_ALL)
        file_writer.writerow(['Ground truth number','Title 1','Title 2','Title 3'])
        for result in resultList:
            if len(result) == 4:
                file_writer.writerow([str(result[0]), str(result[1]), str(result[2]), str(result[3])])

findOutput = list()

with open('createdHITs_find.csv', 'rb') as createdHITs:
    HITreader = csv.reader(createdHITs, csv.excel)
    next(HITreader)
    for HITrow in HITreader:
        path = 'results/HITResultsFor' + str(HITrow[1]) + '.csv'
        if os.path.isfile(path):
            results = list()
            results.append(HITrow[0])
            with open(path, 'rb') as resultHIT:
                Resultsreader = csv.reader(resultHIT, csv.excel, quoting=csv.QUOTE_ALL)
                next(Resultsreader)
                for result in Resultsreader:
                    if str(result[5]).find('Approved') >= 0:                    
                        results.append(result[8])
            findOutput.append(results)
            
createCsvFile('input_title_vote.csv', findOutput)