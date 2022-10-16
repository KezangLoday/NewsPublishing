from flask import Flask, render_template,session,request,redirect
from newsapi import NewsApiClient
import datetime as the_date
from datetime import date
import pyrebase


app = Flask(__name__)


config= {
    'apiKey': "AIzaSyCm_uspbQkt9xt8xh3OGRdQsKQGF0NlR9k",
    'authDomain': "authenticatepy-88ab7.firebaseapp.com",
    'projectId': "authenticatepy-88ab7",
    'storageBucket': "authenticatepy-88ab7.appspot.com",
    'messagingSenderId': "2045932540",
    'appId': "1:2045932540:web:d01778e9e72dc6c3eef879",
    'measurementId': "G-BTHZ66KQES",
    'databaseURL': ""
}

#starting your firebase
firebase = pyrebase.initialize_app(config)
auth= firebase.auth()

app.secret_key='secret'


today = date.today()


#logining into the website
@app.route("/login", methods=['POST','GET'])
def login():
    #if successful login
    
    if('user' in session):
        return redirect('/')
    
    # checking the info 
    if request.method=='POST':
        email= request.form.get('email')
        password=request.form.get('pass')
        try:
            user=auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
        except:
            return 'Failed to Login, Your username or password is incorrect'

    return render_template('Login.html')


#signup
@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':

        email=request.form.get('email2')
        password=request.form.get('pass2')
        confirmpassword=request.form.get('Cpass')
        if confirmpassword==password:
            try:
                user=auth.create_user_with_email_and_password(email, password)
                return redirect('/')

            except:
             return 'your password does not match. Please enter your same password'

    return render_template('signup.html')

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
    my_data = newsapi.get_everything(sources="al-jazeera-english", to=today, sort_by="popularity")
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

# @app.route('/thebhutanese')
# def thebhutanese():
#     newsapi = NewsApiClient(api_key="f8f06d634b0e48f6a9e41363832a25c5")
#     my_data = newsapi.get_everything(sources="cnn", to=today, sort_by="popularity")
#     articles = my_data['articles']
#
#     desc = []
#     news = []
#     img = []
#     author = []
#     time = []
#     url = []
#
#     for i in range(len(articles)):
#         myarticles = articles[i]
#
#         news.append(myarticles['title'])
#         desc.append(myarticles['description'])
#         img.append(myarticles['urlToImage'])
#         author.append(myarticles['author'])
#         url.append(myarticles['url'])
#         pub_date = the_date.datetime.strptime(myarticles['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").date()
#
#         time.append(pub_date.strftime("%B %d, %Y"))
#
#     mylist = zip(news, desc, img, author, time, url)
#
#     return render_template('cnn.html', context=mylist)

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
