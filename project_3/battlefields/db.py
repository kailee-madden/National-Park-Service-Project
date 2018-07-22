#!/usr/bin/env python
'''Tools for working with NPS civil war battlefields database'''

import os
import sys
import json
import sqlite3
import argparse


def dict_factory(cursor, row):
    '''strict dictionary format for rows'''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class BattlesDB(object):
    '''A connection to the battlefields database'''
      
    def __init__(self, data_dir):
        '''A new connection to the database'''
        
        self.db_file = os.path.join(data_dir, "battles.db")
        self.data_file = os.path.join(data_dir, "nps_battlefields.json")
        self.conn = sqlite3.connect(self.db_file)

        self.conn.row_factory = dict_factory
        self._create_table()
        self._populate_table()
        
        # TODO:
        #  - connect to the database
        #  - set the .row_factory attribute to `dict_factory`
        #  - create the Battle table
        #  - populate it with data from the json file 
    
    
    def _create_table(self):
        '''Create the new tables'''

        # TODO
        cur = self.conn.cursor()
        cur.execute('''DROP TABLE IF EXISTS Battle''')

        create_battle = '''CREATE TABLE IF NOT EXISTS Battle(
        battle_id INTEGER PRIMARY KEY,
        us_command TEXT,
        end_date TEXT,
        description TEXT,
        campaign TEXT,
        location TEXT,
        url TEXT,
        cs_command TEXT,
        all_casualties INTEGER,
        cs_casualties INTEGER,
        us_casualties INTEGER,
        state TEXT,
        result INTEGER,
        duration INTEGER,
        start_date TEXT,
        battle_name TEXT


         )'''

        #will need to add to table later, not going to at the moment, have to add battle_id?

        cur.execute(create_battle)

        cur = self.conn.cursor()

    
    
    def _populate_table(self):
        '''Populate the table from the csv file'''
        
        # TODO 
        cur = self.conn.cursor()
        
        with open(self.data_file) as fh:
            data = json.load(fh)
            
            insert_sql = '''
                INSERT INTO Battle VALUES (
                    NULL,
                   :us_command,
                   :end_date,
                   :description,
                   :campaign,
                   :location,
                   :url,
                   :cs_command,
                   :all_casualties,
                   :cs_casualties,
                   :us_casualties,
                   :state,
                   :result,
                   :duration,
                   :start_date,
                   :name
                )'''
            
            cur.executemany(insert_sql, data)


        
        self.conn.commit()
    
    
    def search(self, battle_name, state):
        '''Return battles matching name and state criteria'''
        
        # TODO: return rows that match BOTH criteria
        #   - use LIKE to get partial matches, at least on `battle_name`
        #need to figure out what is meant by rows

        cur = self.conn.cursor()
        
        # sql statement
        sql = '''SELECT * FROM Battle WHERE (battle_name LIKE ?) AND (state LIKE ?) ORDER BY 
            battle_name'''        
        

        cur.execute(sql, ('%' + battle_name +'%', state,))
        return cur.fetchall()

       #May have to edit execute statement
    
    
    def detail(self, battle_id):
        '''Return one row based on exact match of battle_id'''
        
        # TODO
        cur = self.conn.cursor()
        sql = '''SELECT * FROM Battle WHERE battle_id = ?'''

        cur.execute(sql, (battle_id,))
        return cur.fetchone()

        #won't work until add battle_id

    
    def states(self):
        '''Get possible values for the state field'''
        cur = self.conn.cursor()
        state_results = []
        sql = '''SELECT DISTINCT state FROM Battle'''
        cur.execute(sql)
        for state in cur.fetchall():
            state_results.append(state['state'])

        return sorted(state_results)



                    
        # TODO - get the distinct values for `state`
        #      - return it as a list of states, not a list of rows
        
        
        #Don't understand what he's saying here with regard to 
        
# main code block: test the module
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'test the BattlesDB interface'
    )
    parser.add_argument('--name', default='%', help="Value for battle name")
    parser.add_argument('--state', default='%', help="Value for state")
    parser.add_argument('--data', default='data', help="Path to data directory")
    args = parser.parse_args()
    db = BattlesDB(args.data)
    
    print json.dumps(db.search(args.name, args.state), indent=1)