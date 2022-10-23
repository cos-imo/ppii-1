from flask import *

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')



app.run(host='localhost', port=5000)


#test 12