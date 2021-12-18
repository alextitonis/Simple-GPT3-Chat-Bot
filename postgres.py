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
    
    def __login(username, password):
        print()
        
    def __register(username, password):
        print()