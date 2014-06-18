# Master Thesis Source Code
This repository contains the source code of the master thesis with the title 'Crowdsourced Item Descriptions and Price Estimations'. The report of the thesis is accessible under the link https://github.com/steve84/thesis-doc.

## Name conventions
- _mturk*.py_: The files will create one or more HITs for the Amazon Mechanical Turk platform
- _parser*.py_: Information of the HITs will be extracted from the results. The output will be used as an input for other tasks
- _input*.csv_: The results of previous tasks will be used as inputs for subsequent HITs
- _createdHITs*.csv_: The HIT Ids of the created tasks
- _keys.csv_: Stores the credentials of the MTurk platform (Comma separated values)

## Folder structure of the experiments
- _output_ The results of all subtasks (Comma separated values)
	- _dat_ GNUPlot data format
- _tasks_ The tasks for MTurk
	- _title_ Generate a title for an auction item
	- _description_ Describe the item. The folder also contains the TurKit binary file
	- _category_ Categorise the auction item
	- _price_ Find an appropriate price for the object
	- _evaluation_ Determine the performance of the crowd in comparison with the ground truth

## Requirements
To execute the experiments the following steps have to be done:

1. Create an Amazon Mechanical Turk account (http://www.mturk.com)
2. Register to the eBay developers program (https://go.developer.ebay.com)
3. Insert the MTurk credentials into the keys.csv file
4. Replace the INSERT_APP_ID string with the eBay application id in the Python files
5. Install Python (>= v2.7)
6. Install eBay SDK (https://github.com/timotheus/ebaysdk-python)
7. Install boto (https://github.com/boto/boto)
