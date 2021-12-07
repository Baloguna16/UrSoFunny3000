import os
from flask import Flask

app = Flask(__name__)

@app.get("/")
def index():
    return {"data": "I like cheese."}, 200

app.run(host='0.0.0.0', port=os.environ.get('PORT'))
