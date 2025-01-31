from typing import Annotated

from fastapi import Depends,FastAPI
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from dynamodb_client import DynamoDBClient

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
db_client = DynamoDBClient()

@app.get("/getItems")
def read_root():
    response = db_client.get_item_values("76E5549434")
    return response


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}