# -*- coding: utf-8 -*-

from ebaysdk.finding import Connection as Finding
from ebaysdk.shopping import Connection as Shopping
from ebaysdk.exception import ConnectionError
import json, csv, unicodedata, dateutil.parser
from sklearn import cross_validation

def getItemDetails(item, nbr):
    itemId = item['itemId']['value']
		# initialise eBay Shopping API
    api2 = Shopping(appid='INSERT_APP_ID')
    
    try:
				# get item details
        api2.execute('GetSingleItem', {
            'ItemID': str(itemId),
            'IncludeSelector': 'TextDescription,ItemSpecifics,Details,Variations'
            })
    
        response = json.loads(api2.response_json())
    except ConnectionError:
        return 'null'
    
    fields = set(('Description','PictureURL','ConditionDisplayName','ConvertedCurrentPrice','PrimaryCategoryName','Title','ItemSpecifics','Seller','StartTime','EndTime','HandlingTime','GlobalShipping','ReturnPolicy','Quantity'))
    pure_auction = (item['listingInfo']['bestOfferEnabled']['value'] == 'false') & (item['listingInfo']['buyItNowAvailable']['value'] == 'false')
    # check if all needed fields are available    
    if fields.issubset(response['Item'].keys()) & pure_auction:
				# collect the data (features)
        if 'value' in response['Item']['Description'].keys():
            description = unicodedata.normalize('NFKD', response['Item']['Description']['value']).encode('ascii','ignore')
        else:
            description = ''
        pictures = response['Item']['PictureURL']
        condition = convertConditionToNumber(response['Item']['ConditionDisplayName']['value'])
        price = float(response['Item']['ConvertedCurrentPrice']['value'])  
        category = str(response['Item']['PrimaryCategoryName']['value'])
        title = str(unicodedata.normalize('NFKD', response['Item']['Title']['value']).encode('ascii','ignore'))
        if ((title.lower().find('lot') >= 0) | (title.lower().find('set') >= 0) | (title.lower().find('bundle') >= 0)):
            return 'null'
        model = -1
        code = 0
        specifics = response['Item']['ItemSpecifics']['NameValueList']
        seller_rating = float(response['Item']['Seller']['PositiveFeedbackPercent']['value'])
        seller_rating_count = convertRatingStarToNumber(response['Item']['Seller']['FeedbackRatingStar']['value'])
        
        start_time = dateutil.parser.parse(response['Item']['StartTime']['value'])
        end_time = dateutil.parser.parse(response['Item']['EndTime']['value'])
        end_weekday = end_time.isoweekday()
        start_weekday = start_time.isoweekday()
        end_hour = end_time.hour
        if (start_time.hour == end_time.hour) & (start_time.minute == end_time.minute) & (start_time.second == end_time.second):
            duration = (end_time - start_time).days
        else:
            duration = 0

        shipping_locations = convertShipToLocationsToNumber(item['shippingInfo']['shipToLocations'])
        shipping_type = convertShippingTypeToNumber(str(item['shippingInfo']['shippingType']['value']))
        handling_time = int(response['Item']['HandlingTime']['value'])
        global_shipping = 0
        if str(response['Item']['GlobalShipping']['value']) == 'true':
            global_shipping = 1
            
        nbr_of_pictures = len(pictures)
        len_of_description = len(description)
        
        returns_accepted = 1
        if str(response['Item']['ReturnPolicy']['ReturnsAccepted']['value']).find('ReturnsNotAccepted') >= 0:
            returns_accepted = 0
        
        if len(specifics) > 3:
            for entry in specifics:
                if (entry['Name']['value'] == 'Model'):
                    model = convertModelToNumber(entry['Value']['value'], title)
                if (entry['Name']['value'] == 'Region Code'):
                    if isinstance(entry['Value'], dict):
                        code = convertRegionCodeToNumber(entry['Value']['value'], title)
                if (entry['Name']['value'] == 'Bundled Items'):
                    return 'null'
                
        quantity = int(response['Item']['Quantity']['value'])
        # take only items which have more than two images, an assigned model number, the quantity field is 1, ...        
        if (len(description) > 0) & (len(pictures) > 2) & (condition > 0) & (price != 0) & (model >= 0) & (duration > 0) & (seller_rating_count >= 0) & (quantity == 1):
            pictures_list = list()
            for y in range(0,len(pictures)):
                pictures_list.append(str(pictures[y]['value']))
            # save the features to a list    
            item_list = list()
            item_list.append(title) #0
            item_list.append(description) #1
            item_list.append(category) #2
            item_list.append(int(nbr+1)) #3           
            item_list.append(int(itemId)) #4
            item_list.append(condition) #5
            item_list.append(price) #6
            item_list.append(model) #7
            item_list.append(code) #8
            item_list.append(seller_rating) #9
            item_list.append(seller_rating_count) #10
            item_list.append(duration) #11
            item_list.append(nbr_of_pictures) #12
            item_list.append(len_of_description) #13
            item_list.append(end_weekday) #14
            item_list.append(start_weekday) #15
            item_list.append(end_hour) #16
            item_list.append(handling_time) #17
            item_list.append(global_shipping) #18            
            item_list.append(shipping_locations) #19
            item_list.append(shipping_type) #20 
            item_list.append(returns_accepted) #21
            item_list.append(pictures_list) #22
            
            return item_list
        
    return 'null'

# find the number of total pages for a given keyword      
def findTotalItems(api, keyword, categoryId):
    api.execute('findCompletedItems', {
            'keywords': keyword,
            'categoryId': categoryId,
            'itemFilter': [
                {'name': 'ListingType',
                 'value': 'Auction'},
                {'name': 'Currency',
                 'value': 'USD'},                
                {'name': 'SoldItemsOnly',
                 'value': 'true'},                 
            ],
            })
            
    response = json.loads(api.response_json()) 
    return int(response['paginationOutput']['totalPages']['value'])

# get the items of the next page
def getNextPage(api, keyword, categoryId, pageNbr):
    api.execute('findCompletedItems', {
            'keywords': keyword,
            'categoryId': categoryId,
            'itemFilter': [
                {'name': 'ListingType',
                 'value': 'Auction'},
                {'name': 'Currency',
                 'value': 'USD'},                
                {'name': 'SoldItemsOnly',
                 'value': 'true'},                 
            ],
            'paginationInput': [
                {'pageNumber': pageNbr},
            ],
            'sortOrder': 'EndTimeSoonest',              
            })
            
    response = json.loads(api.response_json()) 
    items = response['searchResult']['item']
    return items

# create a html file which contains the collected items      
def createHtmlFile(file_name, itemList):
    f = open(file_name,'w')
    f.writelines('<html><body>')
    f.writelines('<table border=1>')
    f.writelines('<tr><td>ID</td><td>Item ID</td><td>Title</td><td>Description</td><td>Category</td><td>Condition</td><td>Price</td><td>Image 1</td><td>Image 2</td><td>Image 3</td></tr>')
    for item in itemList:
        f.writelines('<tr><td>' + str(item[3]) + '</td><td>' + str(item[4]) + '</td><td>' + str(item[0]) + '</td><td>' + str(item[1]) + '</td><td>' + str(item[2]) + '</td><td>' + str(item[5]) + '</td><td>' + str(item[6]) + '</td><td><img src="' + str(item[22][0]) + '" width="350"></td><td><img src="' + str(item[22][1]) + '"  width="350"></td><td><img src="' + str(item[22][2]) + '" width="350"></td></tr>')
    f.writelines('</table>')
    f.writelines('</body></html>')
    f.close()

# create a csv file which contains the collected items
def createCsvFile(file_name, itemList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel_tab)
        file_writer.writerow(['Title','Description','Category','ID','Item ID','Condition','Price','Model','Region Code','Image 1','Image 2','Image 3'])
        for item in itemList:
            file_writer.writerow([str(item[0]), item[1], str(item[2]), str(item[3]), str(item[4]), str(item[5]), str(item[6]), str(item[7]), str(item[8]), str(item[22][0]), str(item[22][1]), str(item[22][2])])

# create a csv file which contains the collected items (features + labels)            
def createCsvTrainingFile(file_name, dataList, labelList, label=False, val_range=5, normalize=False):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel_tab)
        file_writer.writerow(['Condition','Model','Region Code','Seller rating','Seller rating count','Duration','Number of pictures','Length of description','End Weekday','Start Weekday','End Hour','Handling time','Global shipping','Shipping Locations','Shipping Type','Return accepted','Price'])
				# normalise the features from 0 to 1	
        if not normalize:
            for x in range(0,len(dataList)):
                if label:
                    price_label = int(labelList[x] / val_range) + 1
                else:
                    price_label = float(labelList[x])
                file_writer.writerow([str(dataList[x][0]), str(dataList[x][1]), str(dataList[x][2]), str(dataList[x][3]), str(dataList[x][4]), str(dataList[x][5]), str(dataList[x][6]), str(dataList[x][7]), str(dataList[x][8]), str(dataList[x][9]), str(dataList[x][10]), str(dataList[x][11]), str(dataList[x][12]), str(dataList[x][13]), str(dataList[x][14]), str(dataList[x][15]), str(price_label)])
        else:
            # create min/max values for every feature
            minMaxValues = list()
            minMaxValues.append([1, 6]) #0 Condition
            minMaxValues.append([0, 7]) #1 Model
            minMaxValues.append([0, 3]) #2 Region Code
            minMaxValues.append([0, 100]) #3 Seller rating
            minMaxValues.append([0, 12]) #4 Seller rating count
            minMaxValues.append([1, 10]) #5 Duration
            minMaxValues.append([3, 12]) #6 Number of pictures
            minMaxValues.append([0, 500000]) #7 Length of description
            minMaxValues.append([1, 7]) #8 End wekkday
            minMaxValues.append([1, 7]) #9 Start weekday
            minMaxValues.append([0, 23]) #10 End hour
            minMaxValues.append([0, 20]) #11 Handling time
            minMaxValues.append([0, 1]) #12 Global shipping
            minMaxValues.append([0, 249]) #13 Shipping locations
            minMaxValues.append([0, 7]) #14 Shipping type
            minMaxValues.append([0, 1]) #15 Returns accepted
            
            for x in range(0,len(dataList)):
								# convert the price to a price class (val_range defines class range)
                if label:
                    price_label = int(labelList[x] / val_range) + 1
                else:
                    price_label = float(labelList[x])
                file_writer.writerow([str(normalizeValue(dataList[x][0], minMaxValues[0][0], minMaxValues[0][1])), str(normalizeValue(dataList[x][1], minMaxValues[1][0], minMaxValues[1][1])), str(normalizeValue(dataList[x][2], minMaxValues[2][0], minMaxValues[2][1])), str(normalizeValue(dataList[x][3], minMaxValues[3][0], minMaxValues[3][1])), str(normalizeValue(dataList[x][4], minMaxValues[4][0], minMaxValues[4][1])), str(normalizeValue(dataList[x][5], minMaxValues[5][0], minMaxValues[5][1])), str(normalizeValue(dataList[x][6], minMaxValues[6][0], minMaxValues[6][1])), str(normalizeValue(dataList[x][7], minMaxValues[7][0], minMaxValues[7][1])), str(normalizeValue(dataList[x][8], minMaxValues[8][0], minMaxValues[8][1])), str(normalizeValue(dataList[x][9], minMaxValues[9][0], minMaxValues[9][1])), str(normalizeValue(dataList[x][10], minMaxValues[10][0], minMaxValues[10][1])), str(normalizeValue(dataList[x][11], minMaxValues[11][0], minMaxValues[11][1])), str(normalizeValue(dataList[x][12], minMaxValues[12][0], minMaxValues[12][1])), str(normalizeValue(dataList[x][13], minMaxValues[13][0], minMaxValues[13][1])), str(normalizeValue(dataList[x][14], minMaxValues[14][0], minMaxValues[14][1])), str(normalizeValue(dataList[x][15], minMaxValues[15][0], minMaxValues[15][1])), str(price_label)])                

# function to normalise the features                              
def normalizeValue(value, min_val, max_val):
    return float((float(value) - float(min_val)) / (float(max_val) - float(min_val)))
            
def convertModelToNumber(model, title):
    modelnbr = -1
    model = model.lower()
    title = title.lower()
    if ((model.find('playstation 1') >= 0) & (title.find('1') >= 0)):
        modelnbr = 7
    elif ((model.find('playstation 2') >= 0) & (title.find('2') >= 0)):
        if ((model.find('slim') >= 0) & (title.find('slim') >= 0)):
            modelnbr = 6
        else:
            modelnbr = 5
    elif ((model.find('playstation 3') >= 0) & (title.find('3') >= 0)):
        if ((model.find('slim') >= 0) & (title.find('slim') >= 0)):
            modelnbr = 4
        else:
            modelnbr = 3
    elif ((model.find('playstation 4') >= 0) & (title.find('4') >= 0)):        
        modelnbr = 2
    elif ((model.find('playstation vita') >= 0) & (title.find('vita') >= 0)):        
        modelnbr = 1        
    elif (title.find('psp') >= 0):   
        modelnbr = 0
        
    return int(modelnbr)
    
def convertConditionToNumber(condition):
    conditionnbr = 0
    if (condition.find('New') >= 0):
        conditionnbr = 6
    elif (condition.find('New other') >= 0):
        conditionnbr = 5
    elif (condition.find('Manufacturer refurbished') >= 0):
        conditionnbr = 4
    elif (condition.find('Seller refurbished') >= 0):        
        conditionnbr = 3
    elif (condition.find('Used') >= 0): 
        conditionnbr = 2
    elif (condition.find('For parts or not working') >= 0):
        conditionnbr = 1
        
    return conditionnbr
    
def convertRegionCodeToNumber(region, title):
    regionnbr = 0
    if (region.find('NTSC') >= 0):
        regionnbr = 3
    elif (region.find('PAL') >= 0):
        regionnbr = 2
    elif (region.find('Region Free') >= 0):
        regionnbr = 1
        
    return int(regionnbr)

def convertShippingTypeToNumber(type):
    typenbr = 0
    if (type.find('Calculated') >= 0):
        typenbr = 7
    elif (type.find('CalculatedDomesticFlatInternational') >= 0):
        typenbr = 6
    elif (type.find('Flat') >= 0):
        typenbr = 5
    elif (type.find('FlatDomesticCalculatedInternational') >= 0):
        typenbr = 4
    elif (type.find('Free') >= 0):
        typenbr = 3
    elif (type.find('Freight') >= 0):        
        typenbr = 2
    elif (type.find('CustomCode') >= 0):        
        typenbr = 1        
    else:   
        typenbr = 0
        
    return typenbr
    
def convertRatingStarToNumber(color):
    colornbr = 0
    if (color.find('None') >= 0):
        colornbr = 0
    elif (color.find('Blue') >= 0):
        colornbr = 2
    elif (color.find('CustomCode') >= 0):
        colornbr = -1
    elif (color.find('GreenShooting') >= 0):
        colornbr = 11
    elif (color.find('Green') >= 0):
        colornbr = 6
    elif (color.find('PurpleShooting') >= 0):        
        colornbr = 9
    elif (color.find('Purple') >= 0):        
        colornbr = 4        
    elif (color.find('RedShooting') >= 0):
        colornbr = 10
    elif (color.find('Red') >= 0):
        colornbr = 5
    elif (color.find('SilverShooting') >= 0):
        colornbr = 12
    elif (color.find('TurquoiseShooting') >= 0):
        colornbr = 8
    elif (color.find('Turquoise') >= 0):        
        colornbr = 3
    elif (color.find('YellowShooting') >= 0):        
        colornbr = 7          
    elif (color.find('Yellow') >= 0):        
        colornbr = 1
        
    return colornbr   

def convertShipToLocationsToNumber(loc):
    locnbr = 0
    if not isinstance(loc,list):
        loc = str(loc)
        if (loc.find('Worldwide') >= 0):
            locnbr = 249
        elif (loc.find('WillNotShip') >= 0):
            locnbr = 0
        else:
            locnbr = 1
    else:
        locnbr = len(loc)
        
    return locnbr
     
try:
    api = Finding(appid='INSERT_APP_ID')

		# define keyword and corresponding category id  
    keyword = 'sony playstation'
    categoryId = '139971'
    
    pages = findTotalItems(api, keyword, categoryId) - 1
    pageSize = 100
    minTrainingData = 2200
    
    training_data = list()
    items = list()

		# get next page	    
    for x in range(0,pages):
        items.append(getNextPage(api, keyword, categoryId, x+1))
            
    count = pages * pageSize
    # collect items until the minimal amount of data is reached    
    for x in range(0,pages):
        for y in range(0,pageSize):
            item = getItemDetails(items[x][y],len(training_data))
            if item != 'null':
                training_data.append(item)
        if len(training_data) > minTrainingData:
            break

		# split into features and label data						
    data = list()
    label = list()
    for entry in training_data:
        reduced_entry = entry[5:22]
        p = reduced_entry.pop(1)
        data.append(reduced_entry)
        label.append(entry[6])

		# create a randomised test set of 30%				
    data_train, data_test, label_train, label_test = cross_validation.train_test_split(data,label,test_size=0.3)
    
		# create the data files
    createHtmlFile('groundTruth.html', training_data)
    createCsvFile('groundTruth.csv', training_data)
		# unnormalised for regression
    createCsvTrainingFile('train/trainingData.csv', data_train, label_train)
    createCsvTrainingFile('test/testData.csv', data_test, label_test)
		# unnormalised for classification
    createCsvTrainingFile('train/trainDataLabeled.csv', data_train, label_train, label=True, val_range=25)
    createCsvTrainingFile('test/testDataLabeled.csv', data_test, label_test, label=True, val_range=25)
		# normalised for regression
    createCsvTrainingFile('train/trainingDataNormalized.csv', data_train, label_train, normalize=True)
    createCsvTrainingFile('test/testDataNormalized.csv', data_test, label_test, normalize=True)    
		# normalised for classification
    createCsvTrainingFile('train/trainDataLabeledNormalized.csv', data_train, label_train, label=True, val_range=25, normalize=True)
    createCsvTrainingFile('test/testDataLabeledNormalized.csv', data_test, label_test, label=True, val_range=25, normalize=True)
    
except ConnectionError as e:
    raise e   