import json
from flask import Flask, session, request
import flask
from postgres import postgres
from gpt3 import gpt3
from utils import * 
import envReader

app = Flask('project')
_postgres: postgres = None
_gpt3: gpt3 = None
chat_history = {}

@app.route('/', methods=['POST', 'GET', 'DELETE'])
def main_page():
    try:
        if request.method == 'POST':
            if 'loggin' in request.form:
                username = request.form['username']
                password = request.form['password']
                if _postgres.login(username, password) == True:
                    session['logged_in'] = True
                    session['username'] = username
                return flask.make_response(flask.redirect('/'))
            elif 'register' in request.form:
                print('going to register')
                return flask.make_response(flask.redirect('register'))
        elif request.method == 'GET':
            if session.get('logged_in') == None or session.get('logged_in') == False:
                session['logged_in'] = False
                html = read_file('loggin.html')
                html += '<center>'
                html += '<h4>Login</h4>'
                html += '<form action="/" method="post" id="loggin">'
                html += '<label for="username">Username:</label><br>'
                html += '<input type="text" id="username" name="username" value=""><br>'
                html += '<label for="client">Password:</label><br>'
                html += '<input type="text" id="password" name="password" value=""><br><br>'
                html += '<input type="submit" name="loggin" value="Login">'
                
                html += '<form action="/" method="post" id="register">'
                html += '<input type="submit" name="register" value="register">'
                html += '</center></body></html>'
                return html
            else:
                html = read_file('main.html')
                html += '<h1>This website is used to chat with a GPT3 agent</h1>'
                html += '</body></html>'
                return html
        elif request.method == 'DELETE':
            return json.dumps({'success':False}), 404, {'ContentType':'application/json'}
    except Exception as ex:
        print('error: ', ex)
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'}

@app.route('/register', methods=['POST', 'GET'])
def chat_filter_manager():
    if request.method == 'GET':
        print('get register')
        if session.get('logged_in') != None and session.get('logged_in') == True:
            return flask.make_response(flask.redirect('/'))
        html = read_file('loggin.html')
        html += '<center>'
        html += '<h4>Login</h4>'
        html += '<form action="/register" method="post" id="register">'
        html += '<label for="username">Username:</label><br>'
        html += '<input type="text" id="username" name="username" value=""><br>'
        html += '<label for="client">Password:</label><br>'
        html += '<input type="text" id="password" name="password" value=""><br><br>'
        html += '<input type="submit" name="register" value="Register">'
                
        html += '<form action="/register" method="post" id="back">'
        html += '<input type="submit" name="back" value="back">'
        html += '</center></body></html>'
        return html
    elif request.method == 'POST':
        if session.get('logged_in') != None and session.get('logged_in') == True:
            return json.dumps({'logged_in':False}), 404, {'ContentType':'application/json'}
        if 'back' in request.form:
            return flask.make_response(flask.redirect('/'))
        if 'register' in request.form:
            username = request.form['username'].strip()
            password = request.form['password'].strip()
            res = _postgres.register(username, password)
            if res == True:
                return flask.make_response(flask.redirect('/'))
            else:
                return flask.make_response(flask.redirect('register'))
            #if registration is ok then go to login, otherwise reload and show error


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    if request.method == 'GET':
        if session.get('logged_in') == None or session.get('logged_in') == False:
            return flask.make_response(flask.redirect('/'))
        html = read_file('main.html')
        html += '<center>'
        html += '<h4>Chat</h4>'
        html += getChatHtml()
        html += '<form action="/chat" method="post" id="chatmsg">'
        html += '<label for="client">Message:</label><br>'
        html += '<textarea id="message" name="message" rows="4" cols="50"></textarea><br>'
        html += '<input type="submit" name="chatmsg" value="Send">'
        html += '</center></body></html>'
        return html
    elif request.method == 'POST':
        if session.get('logged_in') == None or session.get('logged_in') == False:
            return json.dumps({'logged_in':False}), 404, {'ContentType':'application/json'}
        if 'chatmsg' in request.form:
            message = request.form['message'].strip()
            username = session['username']
            addChatMessage(username, message)
            resp = _gpt3.getResponse(getChatHistory())
            addChatMessage('bot', resp)
            return flask.make_response(flask.redirect('/chat'))

        return flask.make_response(flask.redirect('/'))

def getChatHtml():
    html = ''
    username = session['username']
    
    if (username not in chat_history or chat_history[username] == None):
        return html
    
    for x in chat_history[username]:
        html += x['sender'] + ': ' + x['message'] + '<br><br>'
        
    html += '<br><br><br><br>'
    return html

def addChatMessage(sender, message):
    username = session['username']
    
    if (username not in chat_history or chat_history[username] == None):
        chat_history[username] = []
        
    chat_history[username].append({'sender':sender, 'message':message})
    print('added new message: ', message, ' session:', session['chat'])

def getChatHistory():
    username = session['username']
    res = ''
    
    if (username not in chat_history or chat_history[username] == None):
        return res
    
    for x in chat_history[username]:
        res += 'Human: ' + x['message'] + '\n'
    
    return res
       
if __name__ == '__main__':
    envReader.read()
    _postgres = postgres()
    _gpt3 = gpt3(envReader.getValue('GPT3_KEY'))
    app.secret_key = 'SDAKFJDSKJFKJsdf498&F&Ffsdf'
    app.run(host=envReader.getValue('IP'), port=envReader.getValue('PORT'))