# -*- coding: utf-8 -*-

import zmq
from wechat_public.logging.log import getlogger
from fetch_express_tracking import fetch_tracking_data
from TrackData import TrackData

def serve(port=5599):

    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind('tcp://*:%d' % port)
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    db = TrackData()
    logger = getlogger('root')

    while True:
        conns = dict(poller.poll(2000))
        if socket in conns:
            data = socket.recv_json()
            if 'track_no' in data:
                no = data['track_no']
                track_data = fetch_tracking_data(no)
                db.updateOrInsert(track_data)
            else:
                logger.info('Invalid data: empty track NO. [%s]' % str(data))

if __name__ == '__main__':
    serve()