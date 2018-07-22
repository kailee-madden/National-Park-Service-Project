#!/usr/bin/env python
'''Web frontend for the NPS Civil War battlefields database'''

# import statements
import os
import json
import tornado.ioloop
import tornado.web
from battlefields.db import BattlesDB

PORT = 8888
ROOT = '.'

class MainHandler(tornado.web.RequestHandler):
    '''Requests for the landing page'''
    def get(self):
        
        self.render('search.html')


class StatesHandler(tornado.web.RequestHandler):
    '''Requests for valid field values'''
    # TODO: write a JSON dictionary
    #  - format: {"data": ["state1", "state2", "state3", ...]}
    def initialize(self, db):
        self.db = db
        
    def get(self):
        state = self.db.states()
        data = {'data':state}
        self.write(data)
    

class SearchHandler(tornado.web.RequestHandler):
    '''Requests for Searches'''
    # TODO: do a search
    # get user parameters for `state` and `name`
    # call the `db.search` method
    # return the list of rows, embedded in a JSON dictionary
    #  i.e. {"data": ["row1", "row2", "row3", ...]}
    def initialize(self, db):
        self.db = db
        
    def get(self):
        state = self.get_argument('state')
        battle = self.get_argument('battle')
        search = self.db.search(battle, state)
        data = {'data':search}
        self.write(data)
     

class DetailHandler(tornado.web.RequestHandler):
    '''Requests for a single record'''

    # TODO: return one row, based on id
    def initialize(self, db):
        self.db = db
    #  - get user param for `battle_id`
    def get(self):
        #  - call `db.details`
        battle_id = self.get_argument("battle_id")
        row = self.db.detail(battle_id) 
    #  - return the single row embedded in a JSON dictionary
    #   ie {"data": row}
        data = {'data': row}
        self.write(data)


# main code block
if __name__ == '__main__':
    db = BattlesDB(os.path.join(ROOT, 'data'))
    
    # create app, register handlers
    app = tornado.web.Application([
            # hookup dynamic content handlers
            (r'/', MainHandler),
            (r'/states', StatesHandler, {'db': db}),
            (r'/search', SearchHandler, {'db': db}),
            (r'/detail', DetailHandler, {'db': db}),
            
            # static content handlers
            (r'/css/(.*)', tornado.web.StaticFileHandler, {'path':'web_content/css'}),
            (r'/js/(.*)', tornado.web.StaticFileHandler, {'path':'web_content/js'}),
        ],
        template_path = os.path.join('web_content', 'html'),
        debug = True
    )

    # run the app
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()