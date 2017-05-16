def lambda_handler(event, context):
    import boto3
    import datetime
    
    from botocore.exceptions import ClientError
    
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    
    orderTable = dynamodb.Table('Order')
    menuTable = dynamodb.Table('PizzaOrder')
    
    orderid=event.get('orderid')
    input=event.get('input')
    print "input selected= ",input
    
    ordersResponse = orderTable.get_item(
        Key = {
            "orderid": event.get('orderid')
        }
    )
    order = ordersResponse['Item']
    
    #Get the menu Id from order record
    menuid=order['menuid']
    print "Menu id in order table= ",menuid

    menuResponse = menuTable.get_item(
        Key = {
            "menuid": menuid
        }
    )
    menu = menuResponse['Item']
    print "Menu=",menu
    if 'orderdetail' in order:
        if 'selection' in order['orderdetail']:
            sizeOptions = menu['size']
            print "sizeOptions=", sizeOptions
            sizeSelected = sizeOptions[int(input)-1]
            print 'sizeSelected=',sizeSelected

            costOptions = menu['price']
            ordercost = costOptions[int(input)-1]
            print 'cost of selected item=',ordercost

            orderTable.update_item(
            Key = {
                "orderid": orderid
            },
            UpdateExpression = 'set order_status = :val1, orderdetail= :val2',
            ExpressionAttributeValues = {
                ':val1': "Processing",
                ':val2':  {'selection' : order['orderdetail']['selection'],'size' : sizeSelected, 'costs' : ordercost,
                 'order_time' : datetime.datetime.now().strftime("%m-%d-%y@%I:%M:%S")}
            }
        )

        returnMsg =  "Your order costs $%s. We will email you when the order is ready. Thank you!" % ordercost
    
    else:
        selectionOptions = menu['selection']
        selectionSelected = selectionOptions[int(input)-1] #if selection is 1 then it represent 0 index 
        print "Selecting the menu option %s for the given order %s" % (selectionSelected, orderid)
    
        orderTable.update_item(
            Key = {
                "orderid": orderid
            },
            UpdateExpression = 'set orderdetail = :val1',
            ExpressionAttributeValues = {
                ':val1': {'selection' : selectionSelected}
            }
        )    
    
        sizeOption = ''         
        for index, value in enumerate(menu['size']):
            sizeOption += str(index+1) + ". " + value + "  " 
    
        returnMsg = "Which size do you want? "  + sizeOption
        
    return returnMsg
