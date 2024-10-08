from flask import Flask

print(__name__)

app = Flask(__name__)

@app.get('/')
def hello():
  return "Hello world"