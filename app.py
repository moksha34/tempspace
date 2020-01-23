from flask import Flask,render_template
from newschannel import *
from collections import defaultdict
from flask_socketio import SocketIO,send,emit
from jinja2 import Environment as env ,FileSystemLoader as fs_loader

app=Flask(__name__)
app.config['SECRET_KEY']="secret!"
socketio=SocketIO(app)
mychannel=Newschannel('cnn')
topnews=mychannel.get_top_news(5)
news_src={}
jinjaenv = env(loader=fs_loader('templates'))
for k in Newschannel.COUNTRY_CODE.keys():
    news_src.update({k: Newschannel.get_all_srcs(k)})


@app.route("/")
def index():
    return render_template("index.html",title="index",articles=topnews,srcs=news_src)

@socketio.on('connected')
def coneected(data):
    print(data)

@socketio.on('newschannel selected')
def newchannel(data):
    newschannel=Newschannel(data["data"])
    newnews=newschannel.get_top_news(5)
    sendnews=''
    for article in newnews:
        sendnews=sendnews+(jinjaenv.get_template('article').render(article=article))
    print(sendnews)    
    emit("news recieved",{"news": sendnews })

if __name__=="__main__":
    socketio.run(app)    