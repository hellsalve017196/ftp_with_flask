from flask import Flask


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./datashak"
app.config['MAX_CONTENT_PATH'] = 1000000
