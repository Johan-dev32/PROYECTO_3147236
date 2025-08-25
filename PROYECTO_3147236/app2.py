from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
<<<<<<< HEAD
    app.run(debug=True)

=======
    app.run(debug=True) 
>>>>>>> 9dd97e1f5c74ccb34608e371e2db37925fea400b
