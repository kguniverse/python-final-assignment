from sanic import Sanic
from sanic.response import json

app = Sanic("server")

@app.post("/data")
def dataHandler(request):
    return json()


class Dao:
    
    def __init__():
        pass
    
    

