import json
import boto3

def lambda_handler(event, context):
    print(event)
    dynamodb = boto3.resource('dynamodb')
    tableName = "DisplayTable-dev"
    table = dynamodb.Table("DisplayTable-dev")
    
    try:
        response = table.get_item(
            Key={
                'display_id' : 1,
            },
            AttributesToGet=[
                "power"
            ]
        )
        # print(response)
        # print(response['Item']['power']) # data check
        
        power = response['Item']['power']
        print(power)
        
        client = boto3.client('iot-data', region_name='ap-northeast-2')
        response = client.publish(
            topic = 'display_power',
            qos = 0,
            payload=json.dumps({"power":power})
        )
    
    except:
        client = boto3.client('iot-data', region_name='ap-northeast-2')
        response = client.publish(
            topic = 'display_power',
            qos = 0,
            payload="data not found"
        )

    return {
        'statusCode' : 200,
        'body' : json.dumps('Hello from Lambda!')
    }