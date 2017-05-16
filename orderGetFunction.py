def lambda_handler(event, context):
    import boto3
    import datetime
    
    from botocore.exceptions import ClientError
    
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    
    orderTable = dynamodb.Table('Order')
    menuTable = dynamodb.Table('PizzaOrder')
    
    orderid=event.get('orderid')
    
    try:
       ordersResponse = orderTable.get_item(
            Key = {
                "orderid": orderid
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        order = ordersResponse['Item']
        print("GetItem succeeded:")
        return order
