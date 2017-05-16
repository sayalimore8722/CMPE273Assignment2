def lambda_handler(event, context):
    import boto3
    import uuid
    
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    
    orderTable = dynamodb.Table('Order')
    menuTable = dynamodb.Table('PizzaOrder')
    
    #order_id=event.get('order_id')
    menuid=event.get('menuid')
    customer_name=event.get('customer_name')
    customer_email=event.get('customer_email')
    
    response = orderTable.put_item(
       Item={
            'orderid': str(uuid.uuid1()),
            'menuid': menuid,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'order_status': 'Processing'
        }
    )
    
    print("PutItem on Order succeeded:")
    menuResponse = menuTable.get_item(
        Key = {
            "menuid": menuid
        }
    )
    menu = menuResponse['Item']

    selectionOption = ''         
    for index, value in enumerate(menu['selection']):
        selectionOption += str(index+1) + ". " + value + "  " 

    returnMsg = "Hi {" + event.get('customer_name') + "}, please choose one of these selection: " + selectionOption
    
    return {
        "message" : returnMsg
    }
