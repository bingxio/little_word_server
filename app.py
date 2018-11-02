# ! /usr/bin/python3
# -*- coding:utf-8 -*-

# Author: Turaiiao
# Email: 1171840237@qq.com

from tornado import web, options, ioloop, httpserver

from logging.handlers import TimedRotatingFileHandler

from datetime import datetime, date

import pymongo

import configparser, os, logging, sys, json, random

PORT = 6264

########## Config log ##########

logFilePath = 'obtain.log'
logger = logging.getLogger('Obtain')
logger.setLevel(logging.DEBUG)
handle = TimedRotatingFileHandler(logFilePath, when = 'D', interval = 1, backupCount = 30)
handle.suffix = '%Y%m%d'
handle.setFormatter(logging.Formatter('%(asctime)s  %(filename)s [line:%(lineno)d] %(levelname)s %(message)s'))
logger.addHandler(handle)

########## Config configuration file ##########

cf = configparser.ConfigParser()
cf.read(os.path.abspath('.') + '/secret.conf')

host = cf.get('MongoDB', 'host')

username = cf.get('MongoDB', 'username')
password = cf.get('MongoDB', 'password')

########## Config MongoDB ##########

client = pymongo.MongoClient(host)

db = client.little_word_db

try:
    db.authenticate(username, password)
    db_obtain_collection = db.obtain_collection
except:
    print ('mongodb server start failed ! \r')
    sys.exit(1)

########## Config utils ##########

def http_response(self, msg, code):
    self.write(json.dumps({
        'msg': msg,
        'code': code
    }))

class JsonDateEncode(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

########## Main logic ##########

class ObtainPOSTHandle (web.RequestHandler):

    def get (self, *args, **kwargs):

        global random_index

        db_obtain_collection_max_index = db_obtain_collection.find().sort('index', pymongo.DESCENDING)

        if db_obtain_collection_max_index is not None:
            try:
                random_index = random.randint(1, int(db_obtain_collection_max_index[0]['index']))
            except:
                logger.info('ObtainPOSTHandle: 500 find random index error !')
                http_response(self, 'find random index error', 500)

            db_obtain_collection_find_with_index = db_obtain_collection.find_one({
                'index': random_index
            })

            if db_obtain_collection_find_with_index is not None:
                self.write(json.dumps({
                    'index': db_obtain_collection_find_with_index['index'],
                    'content': db_obtain_collection_find_with_index['content'],
                    'author': db_obtain_collection_find_with_index['author'],
                    'create_date': db_obtain_collection_find_with_index['create_date']
                }, cls=JsonDateEncode))
            else:
                logger.info('ObtainPOSTHandle: 500 find random index with find_one function return error !')
                http_response(self, '500 find random index with find_one function return error', 500)
        else:
            logger.info('ObtainPOSTHandle: 500 sort max index error !')
            http_response(self, '500 sort max index error', 500)

    def post (self, *args, **kwargs):
        try:
            author = self.get_argument('author')
            content = self.get_argument('content')
        except:
            logger.info('ObtainPOSTHandle: increment argument !')
            http_response(self, 'increment argument', 400)
            return

        db_obtain_collection_max_index = db_obtain_collection.find().sort('index', pymongo.DESCENDING)

        db_obtain_collection_insert_with_index = db_obtain_collection.insert_one ({
            'index': int(db_obtain_collection_max_index[0]['index']) + 1,
            'content': content,
            'author': author,
            'create_date': datetime.now()
        })

        if db_obtain_collection_insert_with_index is not None:
            http_response(self, '200 POST successfully', 200)
        else:
            logger.info('ObtainPOSTHandle: 500 POST error !')
            http_response(self, '500 POST error', 500)

if __name__ == '__main__':

    application = web.Application([
        (r'/', ObtainPOSTHandle)
    ])

    server = httpserver.HTTPServer(application)

    print ('tornado server is ready for service \r')

    options.parse_command_line()
    server.listen(PORT)
    ioloop.IOLoop.instance().start()
