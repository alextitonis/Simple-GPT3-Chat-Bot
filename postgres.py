import psycopg2
import os
from datetime import datetime
from json import dumps
import envReader

class postgres: 
    def __init__(self):
        print('initializing postgres')
        self.postgres_con = psycopg2.connect(
                            host=envReader.getValue('PGHOST'),
                            database=envReader.getValue('PGDATABASE'),
                            user=envReader.getValue('PGUSER'),
                            password=envReader.getValue('PGPASSWORD'))
        self.cur = self.postgres_con.cursor()
    
    def login(self, username, password):
        if (username == '' or password == ''):
            return False
        
        query = """SELECT * FROM accounts WHERE username=%s AND password=%s"""
        self.cur.execute(query, (username, password))
        results = self.cur.fetchall()
        return len(results) > 0
    
    def accountExists(self, username):
        if (username == ''):
            return True
        
        query = """SELECT * FROM accounts WHERE username=%s"""
        self.cur.execute(query, (username))
        results = self.cur.fetchall()
        return len(results) > 0
        
    def register(self, username, password):
        if (username == '' or password == ''):
            return False
        
        if (self.accountExists(username, password) == True):
            return False
        
        query = """INSERT INTO accounts(username, password) VALUES(%s, %s)"""
        self.cur.execute(query, (username, password))
        self.postgres_con.commit()
        return True