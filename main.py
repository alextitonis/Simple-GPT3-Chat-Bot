import json
from flask import Flask, session, request
import flask
from postgres import postgres
from utils import * 
import envReader

app = Flask('project')
postgres: postgres = None

@app.route('/', methods=['GET', 'DELETE'])
def main_page():
    try:
        if request.method == 'POST':
            if 'loggin' in request.form:
                username = request.form['username']
                password = request.form['password']
                if envReader.getValue('MANAGER_USERNAME') == username and envReader.getValue('MANAGER_PASSWORD') == password:
                    session['logged_in'] = True
            elif 'register' in request.form:
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
                html += '</body></html>'
                return html
        elif request.method == 'DELETE':
            return json.dumps({'success':False}), 404, {'ContentType':'application/json'}
    except Exception as ex:
        print('error: ' + ex)
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'}

@app.route('/register', methods=['POST', 'GET'])
def chat_filter_manager():
    if request.method == 'GET':
        if session.get('logged_in') != None and session.get('logged_in') == True:
            return flask.make_response(flask.redirect('/'))
        html = read_file('loggin.html')
        html += '<center>'
        html += '<h4>Login</h4>'
        html += '<form action="/" method="post" id="register">'
        html += '<label for="username">Username:</label><br>'
        html += '<input type="text" id="username" name="username" value=""><br>'
        html += '<label for="client">Password:</label><br>'
        html += '<input type="text" id="password" name="password" value=""><br><br>'
        html += '<input type="submit" name="register" value="Register">'
                
        html += '<form action="/" method="post" id="back">'
        html += '<input type="submit" name="back" value="back">'
        html += '</center></body></html>'
        return html
    elif request.method == 'POST':
        if session.get('logged_in') != None and session.get('logged_in') == True:
            return json.dumps({'logged_in':False}), 404, {'ContentType':'application/json'}
        if 'register' in request.form:
            return flask.make_response(flask.redirect('/'))
        if 'back' in request.form:
            username = request.form['username'].strip()
            password = request.form['password'].strip()
            _postgres.addBadWord(word, rating)
            #if registration is ok then go to login, otherwise reload and show error

        return flask.make_response(flask.redirect('/'))
    
if __name__ == '__main__':
    envReader.read()
    postgres = postgres()
    app.secret_key = 'SDAKFJDSKJFKJsdf498&F&Ffsdf'
    app.run(host=envReader.getValue('BOT_MANAGER_IP'), port=envReader.getValue('BOT_MANAGER_PORT'))