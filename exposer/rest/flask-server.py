from flask import Flask                                                                                                                                                  
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world!'

@app.route('/people/<person>')
def test(person):
    if person:
        return 'Welcom, %s!' % person
    return type(person)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
