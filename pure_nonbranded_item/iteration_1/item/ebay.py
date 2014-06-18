# -*- coding: utf-8 -*-


from ebaysdk.finding import Connection as Finding
from ebaysdk.shopping import Connection as Shopping
from ebaysdk.exception import ConnectionError
import json, time, csv, unicodedata, urllib, os

def getItemDetails(itemId):
    api2 = Shopping(appid='INSERT_APP_ID')
    
    api2.execute('GetSingleItem', {
        'ItemID': str(itemId),
        'IncludeSelector': 'TextDescription,ItemSpecifics'
        })
        

    response = json.loads(api2.response_json())
    
    if set(('Description','PictureURL','ConditionDisplayName','ConvertedCurrentPrice','PrimaryCategoryName','Title')).issubset(response['Item'].keys()):
        if 'value' in response['Item']['Description'].keys():
            description = unicodedata.normalize('NFKD', response['Item']['Description']['value']).encode('ascii','ignore')
        else:
            description = ''
        pictures = response['Item']['PictureURL']
        condition = str(response['Item']['ConditionDisplayName']['value'])
        price = float(response['Item']['ConvertedCurrentPrice']['value'])  
        category = str(response['Item']['PrimaryCategoryName']['value'])
        title = str(response['Item']['Title']['value'])

        
        if (len(description) >= 100) & (len(pictures) > 2) & (len(condition) > 0) & (price != 0):
            pictures_list = list()
            for y in range(0,len(pictures)):
                pictures_list.append(str(pictures[y]['value']))
                
            item_list = list()
            item_list.append(title)
            item_list.append(description)
            item_list.append(category)
            item_list.append(condition)
            item_list.append(price)
            item_list.append(pictures_list)
            
            return item_list
        
    return 'null'
    
def createHtmlFile(file_name, itemList):
    f = open(file_name,'w')
    f.writelines('<html><body>')
    f.writelines('<table border=1>')
    f.writelines('<tr><td>Title</td><td>Description</td><td>Category</td><td>Condition</td><td>Price</td><td>Image 1</td><td>Image 2</td><td>Image 3</td></tr>')
    for item in itemList:
        f.writelines('<tr><td>' + str(item[0]) + '</td><td>' + item[1] + '</td><td>' + str(item[2]) + '</td><td>' + str(item[3]) + '</td><td>' + str(item[4]) + '</td><td><img src="' + str(item[5][0]) + '" width="350"></td><td><img src="' + str(item[5][1]) + '"  width="350"></td><td><img src="' + str(item[5][2]) + '" width="350"></td></tr>')
    f.writelines('</table>')
    f.writelines('</body></html>')
    f.close()

def createCsvFile(file_name, itemList):
    with open(file_name, 'wb') as test_file:
        file_writer = csv.writer(test_file, csv.excel_tab)
        file_writer.writerow(['Title','Description','Category','Condition','Price','Image 1','Image 2','Image 3'])
        for item in itemList:
            file_writer.writerow([str(item[0]), item[1], str(item[2]), str(item[3]), str(item[4]), str(item[5][0]), str(item[5][1]), str(item[5][2])])
            
 
try:
    api = Finding(appid='INSERT_APP_ID')
    
    ground_truth = list()
    
    api.execute('findCompletedItems', {
        'keywords': 'dining table',
        'categoryId': '38204',
        'itemFilter': [
            {'name': 'ListingType',
             'value': 'Auction'},
            {'name': 'Currency',
             'value': 'USD'},                
            {'name': 'SoldItemsOnly',
             'value': 'true'},                 
        ],        
        'sortOrder': 'StartTimeNewest',
        })
        
    time.sleep(5)

    response = json.loads(api.response_json())
    items = response['searchResult']['item']
    count = int(response['searchResult']['count']['value'])
    
    for x in range(0,count):
        item = getItemDetails(int(items[x]['itemId']['value']))
        if item != 'null':
            ground_truth.append(item)
            path = str(len(ground_truth)) + "/"
            if not os.path.exists(path):
                os.makedirs(path)
            urllib.urlretrieve(item[5][0], path + "image_1.jpg")
            urllib.urlretrieve(item[5][1], path + "image_2.jpg")
            urllib.urlretrieve(item[5][2], path + "image_3.jpg")
            break;
    
    createHtmlFile('groundTruth.html', ground_truth)
    createCsvFile('groundTruth.csv', ground_truth)
    
except ConnectionError as e:
    raise e   