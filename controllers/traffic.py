# -*- coding: utf-8 -*-
# traffic data

def record():
    if len(request.args) > 0:
        req = request.args[0]
    if request.method == 'GET':
        reqObj = dict(
            camera_id=int(request.get_vars['camera_id']),
            lane_number=int(request.get_var['lane_number']),
            datetime_start=int(request.get_vars['datetime_start']),
            datetime_end=int(request.get_vars['datetime_end'])
        )
    else:
        return ""