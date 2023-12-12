from flask import Flask, render_template
from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/views")


@app.route('/')
def home():  # put application's code here
    return render_template('home.html')


@app.route('/home')
def home2():  # put application's code here
    return 'Test'


if __name__ == '__main__':
    app.run(debug=True, port=5000)
