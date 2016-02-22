import pymongo
from conf import conf

class TrackData(object):

    db_colletion = 'track_data'
    db_name = 'express'
    default_limit = 20
    required_fields = [u'track_no', u'time', u'status', u'state', u'from', u'to', u'data', u'packages', u'usetime']

    def __init__(self):
        mongodb_conf = conf['mongodb']
        self.db_host = mongodb_conf.get('host', 'localhost')
        self.db_port = mongodb_conf.get('port', 27017)
        self.db_name = self.db_name
        self.client = pymongo.MongoClient(host=self.db_host, port=self.db_port)
        # self.db = self.client[self.db_name]
        self.db = self.client[self.db_name]
        self.collection = self.db[self.db_colletion]


    def find_one(self, track_no):
        r = self.collection.find_one({'track_no': track_no})
        if r is None:
            r = {'track_no': track_no, 'status': 0}
        return r

    def exist(self, track_no):
        c = self.collection.count({'track_no': track_no})
        return c > 0

    def update(self, track_no, data):
        self.collection.update_one({'track_no': track_no}, data)

    def updateOrInsert(self, data):
        no = data['track_no']
        if self.exist(no):
            self.update(no, data)
        else:
            self.collection.insert(data)
