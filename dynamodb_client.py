import boto3
import os
from dotenv import load_dotenv

load_dotenv()

class DynamoDBClient:
    def __init__(self):
        self._validate_env_vars()
        
        self.client = boto3.resource(
            "dynamodb",
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        self.table = self.client.Table("DevicesData")

    def _validate_env_vars(self):
        required_vars = ["AWS_REGION", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
        for var in required_vars:
            if not os.getenv(var):
                raise ValueError(f"Se necesita esta credencial: {var}")

    def get_item_values(self, device_id, quantity):
        try:
            response = self.table.query(
                KeyConditionExpression="ID = :device_id",
                ExpressionAttributeValues={
                    ":device_id": device_id
                }  ,
                ScanIndexForward=False,  
                Limit=quantity
            )
            item = response.get("Items")
            if not item:
                print(f"El item no fue encontrado: {device_id}")
                return None  

            return item
        except Exception as e:
            print(f"Error Inesperado: {e}")
            return None
