# -*- coding: utf-8 -*-

import csv, os

def createImageTable(imageFolder, nbr, cols):
    htmlImageTable = ""
    htmlImageTable += '<table border=\"0\">'
    path = imageFolder + str(nbr) + '/'
    nbrImages = len([name for name in os.listdir(path)]) - 1
    pos = 0
    for x in range(0, nbrImages):
        if (pos % cols) == 0:
            htmlImageTable += '<tr>'
        link = 'http://pegasus84.noip.me/www/unibe/thesis/' + str(nbr) + '/image_'+ str(x+1) + '.JPG'
        htmlImageTable += '<td><img src="' + str(link) + '" alt="Image ' + str(x+1) + '" width="250" border="2"></img><br /><br />'
        htmlImageTable += '<a href="' + str(link) + '" target="_blank">Link to full size image ' + str(x+1) + ' (new window)</a></td>'
        if (pos % cols) == (cols - 1):
            htmlImageTable += '</tr>'
        pos += 1
    if ((pos % cols) < cols):
        if (pos % cols) == 0:
            htmlImageTable += '<tr>'
        for x in range(0,(cols - (pos % cols))):
            htmlImageTable += '<td></td>'
        htmlImageTable += '</tr>'
            
    htmlImageTable += '</table>'
    return htmlImageTable   
    
def createWorkerTable(workerFile, cols):
    htmlWorkerTable = ""
    htmlWorkerTable += '<table border=\"1\">'
    with open(workerFile, 'rb') as csvfile:
        reader = csv.reader(csvfile, csv.excel_tab)
        next(reader)
        pos = 0
        for row in reader:
            if (pos % cols) == 0:
                htmlWorkerTable += '<tr>'
            htmlWorkerTable += '<td>' + str(row[0]) + '</td>'
            if (pos % cols) == (cols - 1):
                htmlWorkerTable += '</tr>'
            pos += 1
        if ((pos % cols) < cols):
            if not (pos % cols) == 0:
                for x in range(0,(cols - (pos % cols))):
                    htmlWorkerTable += '<td></td>'
                htmlWorkerTable += '</tr>'
            
    htmlWorkerTable += '</table>'
    return htmlWorkerTable 
    
with open('../../../../../ground_truth/groundTruth.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, csv.excel_tab)
    next(reader)
    count = 0
    for row in reader:
        count += 1
        html_code = ""
        html_code += 'All the workers who have done a similar task in the past are excluded from this HIT. If you find your worker ID in the following table, your work <b>will be rejected</b>.'
        html_code += '<br /><br />'         
        html_code += createWorkerTable('../workerIds.csv', 5)
        html_code += '<hr />'        
        html_code += createImageTable('../../../../../ground_truth/large_images/', count, 5)
        with open(str(count) + "/item_" + str(count) + ".js", "wb") as fout:
            with open("template.js", "rb") as fin:
                for line in fin:
                    if line.find('ImageTable') >= 0:
                        fout.write(line.replace('ImageTable', str(html_code)))
                    else:
                        fout.write(line)                        
                    
