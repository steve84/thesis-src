# -*- coding: utf-8 -*-

import csv

def createCsvFile(file_name, resultList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel, quoting=csv.QUOTE_ALL)
        file_writer.writerow(['WorkerId'])
        for result in resultList:
            file_writer.writerow([str(result)])

def findWorkers(inputPath, inputFile):
    workerOutput = list()
    
    with open(inputPath + '/' + inputFile, 'rb') as input_file:
        for line in input_file:
            if line.find('workerId') >= 0:
                line_split = line.split('"')
                workerOutput.append(line_split[3])
                
    return workerOutput

for x in range(1,8):
    workerIds =  findWorkers('turkit/' + str(x) + '/','item_' + str(x) + '.js.database')           
    createCsvFile('../../../../pure_with_commission/iteration_1/tasks/description/turkit/' + str(x) + '/workerIds.csv', set(workerIds))