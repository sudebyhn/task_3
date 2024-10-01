import json
import boto3
from botocore.exceptions import ClientError

# DynamoDB'ye bağlan
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MyTable')  # 'MyTable' tablo isminiz

def lambda_handler(event, context):
    try:
        # Gelen JSON verilerini kontrol et
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps('Request body is missing')
            }
        
        body = json.loads(event['body'])

        # JSON verilerini doğrula
        if 'id' not in body or 'value' not in body:
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid input')
            }
        
        # Verileri DynamoDB'ye ekle
        table.put_item(
            Item={
                '100': body['id'],  # Partition key olarak '100' kullanılıyor
                'value': body['value']
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Data saved successfully')
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error saving data: {str(e)}')
        }
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Error parsing JSON: {str(e)}')
        }
