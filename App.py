from flask import Flask, render_template, session, request, redirect,flash,url_for
from newsapi import NewsApiClient
import datetime as the_date
from datetime import date
import tweepy
import configparser
import pyrebase


app = Flask(__name__)

#firbase config
config= {
    'apiKey': "AIzaSyDktl8sfhBIe6-vq2xM9va7Qie-DOlE6uA",
    'authDomain': "authenticatepy-532b9.firebaseapp.com",
    'projectId': "authenticatepy-532b9",
    'storageBucket': "authenticatepy-532b9.appspot.com",
    'messagingSenderId': "283881868950",
    'appId': "1:283881868950:web:84cd06e2b1c237e25d3cb7",
    'measurementId': "G-XSZQD45572",
    'databaseURL': "https://authenticatepy-532b9-default-rtdb.asia-southeast1.firebasedatabase.app/"
}

#starting your firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()

app.secret_key = 'secret'

today = date.today()


# logining into the website
@app.route("/login", methods=['POST', 'GET'])
def login():
    # if successful login

    #if ('user' in session):
        #return redirect('/')

    # checking the info
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return redirect('/')
        except:
            return 'Failed to Login, Your username or password is incorrect'

    return render_template('Login.html')


# signup
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':

        email = request.form.get('email2')
        password = request.form.get('pass2')
        confirmpassword = request.form.get('Cpass')
        if confirmpassword == password:
            try:
                user = auth.create_user_with_email_and_password(email, password)
                return redirect('/')

            except:
                return 'your password does not match. Please enter your same password'

    return render_template('signup.html')

today = date.today()
#getting todays date so that it can be passed to the API to get the latest News


@app.route('/aboutus')
def aboutus():
    all_data= db.child("feedData").get()
    
    
    return render_template('aboutus.html',employees= all_data)

#inserting data
@app.route('/insert',methods=['POST'])
def insert():
    if request.method== 'POST':
        name= request.form['name']
        email= request.form['email']
        feed= request.form['feed']
    
    my_data={'name':name,'email':email,'feedback':feed}
    db.child("feedData").push(my_data)
    
    #message input in html
    flash("Feedback added successful")

    return redirect(url_for('aboutus'))


#update the details
@app.route('/update',methods=['GET','POST'])
def update():
    if request.method== 'POST':
        my_data= request.form.get('id')

        name= request.form['name']
        email= request.form['email']
        feed= request.form['feed']

        db.child("feedData").child(my_data).update( { "name": name, "email": email, "feedback":feed })

      
        
        flash("Feedback update successful")

        return redirect(url_for('aboutus')) 

        
#delete data

@app.route('/delete/<id>/', methods=['GET','POST'])
def delete(id):
    my_data= id
    db.child("feedData").child(my_data).remove()

    flash("Employee deleted successful")

    return redirect(url_for('aboutus'))


@app.route('/')
def index():
    newsapi = NewsApiClient(api_key="b0f75ce660c0466a9a98c2478f8abb62")
    my_data = newsapi.get_everything(sources="bbc-news", to=today, sort_by="popularity")
    articles = my_data['articles']

    desc = []
    news = []
    img = []
    author = []
    time = []
    url = []

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        author.append(myarticles['author'])
        url.append(myarticles['url'])
        pub_date = the_date.datetime.strptime(myarticles['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").date()

        time.append(pub_date.strftime("%B %d, %Y"))

    mylist = zip(news, desc, img, author, time, url)

    return render_template('index.html', context=mylist)


@app.route('/cnn')
def cnn():
    newsapi = NewsApiClient(api_key="f8f06d634b0e48f6a9e41363832a25c5")
    my_data = newsapi.get_everything(sources="cnn", to=today, sort_by="popularity")
    articles = my_data['articles']

    desc = []
    news = []
    img = []
    author = []
    time = []
    url = []

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        author.append(myarticles['author'])
        url.append(myarticles['url'])
        pub_date = the_date.datetime.strptime(myarticles['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").date()

        time.append(pub_date.strftime("%B %d, %Y"))

    mylist = zip(news, desc, img, author, time, url)

    return render_template('cnn.html', context=mylist)


@app.route('/aljazeera')
def aljazeera():
    newsapi = NewsApiClient(api_key="f8f06d634b0e48f6a9e41363832a25c5")
    my_data = newsapi.get_everything(q="crypto", sources="al-jazeera-english", to=today, sort_by="popularity")
    articles = my_data['articles']
    desc = []
    news = []
    img = []
    author = []
    time = []
    url = []

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        author.append(myarticles['author'])
        url.append(myarticles['url'])
        pub_date = the_date.datetime.strptime(myarticles['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").date()

        time.append(pub_date.strftime("%B %d, %Y"))

    mylist = zip(news, desc, img, author, time, url)

    return render_template('aljazeera.html', context=mylist)





@app.route('/thebhutanese')
def thebhutanese():
    return render_template('theBhutanese.html')

@app.route('/bbs')
def bbs():
    return render_template('bbs.html')


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)


