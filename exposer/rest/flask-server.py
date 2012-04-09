from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/people/<person>')
def test(person):
    if person:
        return 'bienvenue, %s!' % person
    return type(person)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
