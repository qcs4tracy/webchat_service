# -*- coding: utf-8 -*-

import zmq
from wechat_public.logging.log import getlogger
from fetch_express_tracking import fetch_tracking_data
from TrackData import TrackData
from collections import deque

work_que = deque()
_one_second = 1000

def serve(port=5599):

    idle = 0
    gap = 3

    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind('tcp://*:%d' % port)
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    db = TrackData()
    logger = getlogger('root')

    while True:
        conns = dict(poller.poll(_one_second/4))
        if conns:
            idle -= 1
            idle = max(idle, 0)
            if socket in conns:
                data = socket.recv_json()
                print data
                continue
                if 'track_no_list' in data:
                    logger.info('adding [%s]' % ', '.join(data['track_no_list']))
                    for no in data['track_no_list']:
                        work_que.append({'track_no': no})
                else:
                    logger.info('Invalid data: empty track NO. [%s]' % str(data))
        else:
            idle += 1

        if idle >= gap:
            if work_que:
                record = work_que.popleft()
                no = record['track_no']
                track_data = fetch_tracking_data(no)
                db.updateOrInsert(track_data)
            idle = min(idle, gap)


if __name__ == '__main__':
    serve()