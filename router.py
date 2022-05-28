from fastapi import FastAPI
from pyrogram import Client, filters, enums, idle
import socket, pyrogram
from flask import Flask, redirect, render_template, request, url_for
from utils import Session, Request

flask = Flask(__name__, template_folder="templates")
fastapi = FastAPI()

get_session = lambda: Session(ip=socket.gethostbyname(socket.gethostname()))
get_ip = lambda: socket.gethostbyname(socket.gethostname())

@flask.route("/")
def index():
    session = get_session().get()
    if session.is_active:
        return render_template("logged_index.html", session=session)
    return "Hello, you've connected with %s ip address but you didnt logged in yet.\nClick <a href='/login' target='_blank' style='text-decoration:none;color:red;'>here</a> to go login page." % session.ip

@flask.route("/login/<status>")
def login_status(status):
    session = get_session().get()
    if status == "new":
        session.is_active = 0
        session.update()
        return render_template("login.html")
    else:
        return render_template("login.html")
@flask.route("/login")
def login():
    session = get_session().get()
    if session.is_active:
        return "You already have a session. If you want to login again, click <a href='/login/new' target='_blank' style='text-decoration:none;color:red;'>here</a> . (This option removes current user session) "
    return render_template("login.html")
@flask.route("/check/<job>", methods=["POST"])
def check(job: str):
    user_ip = get_ip()
    REQUEST = Request(request.method)
    match job:
        case "login":
            if REQUEST.POST:
                api_id = int(request.form.get("api_id"))
                api_hash = request.form.get("api_hash")
                bot_token = request.form.get("bot_token")
                try:
                    is_userbot = request.form.get("is_userbot")
                except:
                    is_userbot = False
                session = Session(ip=user_ip, api_id=api_id, api_hash=api_hash, bot_token=bot_token if not is_userbot else "", is_active=1)
                if session.get().is_active:
                    session.insert()
                    print(session.update().api_hash)
                else:
                    session.insert()
                return redirect("/")
            else:
                return "end"
        case "logout":
            session = Session(ip=user_ip).update()
            return redirect("/")

@flask.route("/get")
def test():
    session = get_session().get()
    if session.is_active:
        return render_template("logged_index.html", session=session)
    return render_template("index.html")


@flask.route("/api/<method>/", methods=["GET", "POST"])
async def methods_begin(method: str):
    session = Session(ip=get_ip()).get()
    api = Client(name=f"{session.ip}", api_id=session.api_id, api_hash=session.api_hash, bot_token=session.bot_token)
    if not session.has_session:
        return redirect("/")
    else:
        REQUEST = Request(request.method)
        if REQUEST.POST:
            match method:
                case "send_message":
                    print("sd"*5)
                    _method = api.__getattribute__("send_message")
                    with api:
                        d = await api.send_message(**dict(request.form))
                        #_method()
                        await api.start()
                        await api.stop()
            return "sent"
                    
                    
                    
        else:
            return render_template("send_message.html")
        
    
    
        


@flask.route("/api", methods=["POST"])
def api_begin():
    return




flask.run(debug=True)