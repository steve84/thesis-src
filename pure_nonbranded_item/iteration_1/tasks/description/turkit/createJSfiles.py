# -*- coding: utf-8 -*-

import csv


with open('../../../item/groundTruth.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, csv.excel_tab)
    next(reader)
    count = 0
    for row in reader:
        count += 1
        with open(str(count) + "/item_" + str(count) + ".js", "wb") as fout:
            with open("template.js", "rb") as fin:
                for line in fin:
                    if line.find('image1') >= 0:
                        fout.write(line.replace('image1', str(row[5])))
                    elif line.find('image2') >= 0:
                        fout.write(line.replace('image2', str(row[6])))
                    elif line.find('image3') >= 0:
                        fout.write(line.replace('image3', str(row[7])))
                    else:
                        fout.write(line)                        
                    
