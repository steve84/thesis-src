# -*- coding: utf-8 -*-

import csv, os.path, datetime

def createCsvFile(file_name, resultList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel, quoting=csv.QUOTE_ALL)
        file_writer.writerow(['Ground truth number','Description','Length of description','Average working time (Writing)','Average finishing time (Writing)','Average reaction time (Writing)','Average working time (Voting)','Average finishing time (Voting)','Average reaction time (Voting)'])
        for result in resultList:
            if len(result) == 9:
                file_writer.writerow([str(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]), str(result[5]), str(result[6]), str(result[7]), str(result[8])])
                
def createDatFile(file_name, resultList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel_tab, quoting=csv.QUOTE_NONE)
        file_writer.writerow(['#Ground truth number','Length of description','Average working time (Writing)','Average finishing time (Writing)','Average reaction time (Writing)','Average working time (Voting)','Average finishing time (Voting)','Average reaction time (Voting)'])
        for result in resultList:
            if len(result) == 9:
                file_writer.writerow([str(result[0]), str(result[2]), str(result[3]), str(result[4]), str(result[5]), str(result[6]), str(result[7]), str(result[8])])                
                
def getTimesFromDatabase():
    with open('../../item/groundTruth.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, csv.excel_tab)
        next(reader)
        count = 0
        avgWritingWorkingTime = list()
        avgWritingFinishingTime = list()
        avgWritingReactionTime = list()        
        avgVotingWorkingTime = list()
        avgVotingFinishingTime = list()
        avgVotingReactionTime = list()        
        for row in reader:
            count += 1
            with open("turkit/" + str(count) + "/item_" + str(count) + ".js.database", "rb") as fout:
                hitCount = 0
                newHitCount = 0
                assignments = 0
                tmpAssignments = 0
                creationTime = 0
                acceptTime = 0
                submitTime = 0
                workingTime = list()
                finishingTime = list()
                reactionTime = list()
                nbrOfVotes = list()                
                for line in fout:
                    if hitCount == 0:
                        if (line.find('"returnValue" : {') >= 0):
                            newHitCount = 1
                    if hitCount == 1:
                        if (line.find('creationTime') >= 0):
                            line = line.split(' : ')
                            line = line[1].split(',')
                            creationTime = float(line[0])
                        elif (line.find('acceptTime') >= 0):
                            line = line.split(' : ')
                            line = line[1].split(',')
                            acceptTime = float(line[0])
                        elif (line.find('submitTime') >= 0):
                            line = line.split(' : ')
                            line = line[1].split(',')                            
                            submitTime = float(line[0])
                            workingTime.append(datetime.datetime.fromtimestamp(submitTime / 1000) - datetime.datetime.fromtimestamp(acceptTime / 1000))
                            finishingTime.append(datetime.datetime.fromtimestamp(submitTime / 1000) - datetime.datetime.fromtimestamp(creationTime / 1000))
                            reactionTime.append(datetime.datetime.fromtimestamp(acceptTime / 1000) - datetime.datetime.fromtimestamp(creationTime / 1000))
                            newHitCount = 2                            
                    if hitCount == 2:
                        if (line.find('"returnValue" : {') >= 0):
                            newHitCount = 3
                    if hitCount == 3:
                        if (line.find('creationTime') >= 0):
                            line = line.split(' : ')
                            line = line[1].split(',')                            
                            creationTime = float(line[0])
                        elif (line.find('acceptTime') >= 0):
                            line = line.split(' : ')
                            line = line[1].split(',')
                            acceptTime = float(line[0])
                        elif (line.find('submitTime') >= 0):
                            line = line.split(' : ')
                            line = line[1].split(',')
                            submitTime = float(line[0])  
                            workingTime.append(datetime.datetime.fromtimestamp(submitTime / 1000) - datetime.datetime.fromtimestamp(acceptTime / 1000))
                            finishingTime.append(datetime.datetime.fromtimestamp(submitTime / 1000) - datetime.datetime.fromtimestamp(creationTime / 1000)) 
                            reactionTime.append(datetime.datetime.fromtimestamp(acceptTime / 1000) - datetime.datetime.fromtimestamp(creationTime / 1000))
                            newHitCount = 4   
                    if hitCount == 4:
                        if (line.find('maxAssignments') >= 0):
                            parts = line.split(' : ')
                            parts = parts[1].split(',')
                            assignments = int(parts[0])
                            tmpAssignments = 0
                            newHitCount = 5
                    if hitCount == 5:
                        if (line.find('creationTime') >= 0):
                            line = line.split(' : ')
                            line = line[1].split(',')                            
                            creationTime = float(line[0])
                        elif (line.find('acceptTime') >= 0):
                            line = line.split(' : ')
                            line = line[1].split(',')                            
                            acceptTime = float(line[0])
                        elif (line.find('submitTime') >= 0):
                            line = line.split(' : ')
                            line = line[1].split(',')
                            submitTime = float(line[0])
                            workingTime.append(datetime.datetime.fromtimestamp(submitTime / 1000) - datetime.datetime.fromtimestamp(acceptTime / 1000))
                            finishingTime.append(datetime.datetime.fromtimestamp(submitTime / 1000) - datetime.datetime.fromtimestamp(creationTime / 1000))                            
                            reactionTime.append(datetime.datetime.fromtimestamp(acceptTime / 1000) - datetime.datetime.fromtimestamp(creationTime / 1000))
                            tmpAssignments += 1
                            if tmpAssignments == assignments:
                                newHitCount = 6
                    if hitCount == 6:
                        if (line.find('"returnValue" : {') >= 0):
                            newHitCount = 7
                    if hitCount == 7:
                        if (line.find('maxAssignments') >= 0):
                            parts = line.split(' : ')
                            parts = parts[1].split(',')
                            assignments = int(parts[0])
                            if assignments > 1:
                                for x in range(0,tmpAssignments):
                                    workingTime.pop()
                                    finishingTime.pop()  
                                if assignments > 3:
                                    if len(nbrOfVotes) >= 1:
                                        nbrOfVotes.pop()                                  
                                tmpAssignments = 0                                    
                                newHitCount = 5
                            else:
                                nbrOfVotes.append(tmpAssignments)
                                newHitCount = 8
                    if hitCount == 8:
                        if (line.find('creationTime') >= 0):
                            line = line.split(' : ')
                            line = line[1].split(',')                            
                            creationTime = float(line[0])
                        elif (line.find('acceptTime') >= 0):
                            line = line.split(' : ')
                            line = line[1].split(',')
                            acceptTime = float(line[0])
                        elif (line.find('submitTime') >= 0):
                            line = line.split(' : ')
                            line = line[1].split(',')                            
                            submitTime = float(line[0])
                            workingTime.append(datetime.datetime.fromtimestamp(submitTime / 1000) - datetime.datetime.fromtimestamp(acceptTime / 1000))
                            finishingTime.append(datetime.datetime.fromtimestamp(submitTime / 1000) - datetime.datetime.fromtimestamp(creationTime / 1000))
                            reactionTime.append(datetime.datetime.fromtimestamp(acceptTime / 1000) - datetime.datetime.fromtimestamp(creationTime / 1000))
                            newHitCount = 9     
                    if hitCount == 9:
                        if (line.find('maxAssignments') >= 0):
                            parts = line.split(' : ')
                            parts = parts[1].split(',')
                            assignments = int(parts[0])
                            tmpAssignments = 0
                            newHitCount = 10
                    if hitCount == 10:
                        if (line.find('creationTime') >= 0):
                            line = line.split(' : ')
                            line = line[1].split(',')
                            creationTime = float(line[0])
                        elif (line.find('acceptTime') >= 0):
                            line = line.split(' : ')
                            line = line[1].split(',')                            
                            acceptTime = float(line[0])
                        elif (line.find('submitTime') >= 0):
                            line = line.split(' : ')
                            line = line[1].split(',')                            
                            submitTime = float(line[0])
                            workingTime.append(datetime.datetime.fromtimestamp(submitTime / 1000) - datetime.datetime.fromtimestamp(acceptTime / 1000))
                            finishingTime.append(datetime.datetime.fromtimestamp(submitTime / 1000) - datetime.datetime.fromtimestamp(creationTime / 1000))
                            reactionTime.append(datetime.datetime.fromtimestamp(acceptTime / 1000) - datetime.datetime.fromtimestamp(creationTime / 1000))
                            tmpAssignments += 1
                            if tmpAssignments == assignments:
                                nbrOfVotes.append(assignments)
                                newHitCount = 11                             
                    if hitCount == 11:
                        if (line.find('"returnValue" : {') >= 0):
                            newHitCount = 12
                    if hitCount == 12:
                        if (line.find('maxAssignments') >= 0):
                            parts = line.split(' : ')
                            parts = parts[1].split(',')
                            assignments = int(parts[0])
                            if assignments > 1:
                                for x in range(0,tmpAssignments):
                                    workingTime.pop()
                                    finishingTime.pop()
                                if assignments > 3:
                                    nbrOfVotes.pop()
                                tmpAssignments = 0
                                newHitCount = 10
                           
                    hitCount = newHitCount
            avgWritingWorkingTime.append((float((workingTime[0] + workingTime[1] + workingTime[1 + nbrOfVotes[0] + 1]).seconds) / 3))
            avgWritingFinishingTime.append((float((finishingTime[0] + finishingTime[1] + finishingTime[1 + nbrOfVotes[0] + 1]).seconds) / 3))
            avgWritingReactionTime.append((float((reactionTime[0] + reactionTime[1] + reactionTime[1 + nbrOfVotes[0] + 1]).seconds) / 3))
            avgVotingWorkingTime.append(((float((sum(workingTime[2:5]) + sum(workingTime[(2 + nbrOfVotes[0] + 1):(2 + nbrOfVotes[0] + 4)])).seconds) / 4)))
            avgVotingFinishingTime.append(((float((sum(finishingTime[2:5]) + sum(finishingTime[(2 + nbrOfVotes[0] + 1):(2 + nbrOfVotes[0] + 4)])).seconds) / 4)))            
            avgVotingReactionTime.append(((float((sum(reactionTime[2:5]) + sum(reactionTime[(2 + nbrOfVotes[0] + 1):(2 + nbrOfVotes[0] + 4)])).seconds) / 4)))            
#            avgVotingWorkingTime.append(((float((sum(workingTime[2:(2 + nbrOfVotes[0])]) + sum(workingTime[(2 + nbrOfVotes[0] + 1):(2 + nbrOfVotes[0] + nbrOfVotes[1] + 1)])).seconds) / (nbrOfVotes[0] + nbrOfVotes[1]))))
#            avgVotingFinishingTime.append(((float((sum(finishingTime[2:(2 + nbrOfVotes[0])]) + sum(finishingTime[(2 + nbrOfVotes[0] + 1):(2 + nbrOfVotes[0] + nbrOfVotes[1] + 1)])).seconds) / (nbrOfVotes[0] + nbrOfVotes[1]))))
#            avgVotingFinishingTime.append(((float((sum(reactionTime[2:(2 + nbrOfVotes[0])]) + sum(reactionTime[(2 + nbrOfVotes[0] + 1):(2 + nbrOfVotes[0] + nbrOfVotes[1] + 1)])).seconds) / (nbrOfVotes[0] + nbrOfVotes[1]))))            
        return avgWritingWorkingTime, avgWritingFinishingTime, avgWritingReactionTime, avgVotingWorkingTime, avgVotingFinishingTime, avgVotingReactionTime
                
descriptionOutput = list()
avgWritingWorkingTime, avgWritingFinishingTime, avgWritingReactionTime, avgVotingWorkingTime, avgVotingFinishingTime, avgVotingReactionTime = getTimesFromDatabase()

with open('createdHITs.csv', 'rb') as createdHITs:
    HITreader = csv.reader(createdHITs, csv.excel)
    next(HITreader)
    count = 0
    for HITrow in HITreader:
        path = 'results/HITResultsFor' + str(HITrow[1]) + '.csv'
        if os.path.isfile(path):
            results = list()
            with open(path, 'rb') as resultHIT:
                Resultsreader = csv.reader(resultHIT, csv.excel, quoting=csv.QUOTE_ALL)
                next(Resultsreader)
                for result in Resultsreader:
                    results.append(result[8])
            descriptionOutput.append([str(HITrow[0]),str(results[0]), str(len(results[0].replace('\r\n',''))), str(avgWritingWorkingTime[count]), str(avgWritingFinishingTime[count]), str(avgWritingReactionTime[count]), str(avgVotingWorkingTime[count]), str(avgVotingFinishingTime[count]), str(avgVotingReactionTime[count])])
            count += 1
            
createCsvFile('../price/input_description_price.csv', descriptionOutput)
createCsvFile('../evaluation/input_description_evaluation.csv', descriptionOutput)
createCsvFile('../../output/output_description.csv', descriptionOutput)
createDatFile('../../output/dat/output_description.dat', descriptionOutput)