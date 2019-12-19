# -*- coding: utf-8 -*-
# traffic data

import json


def records_in_timegap():
    if request.method == 'GET':
        datetime_start = int(request.get_vars['datetime_start'])
        datetime_end = int(request.get_vars['datetime_end'])
        camera_id = -1
        lane_number = -1
        dt_condition = ((db.vehicle_records.checkPointTime>=datetime_start) & (db.vehicle_records.checkPointTime<datetime_end))
        camera_condition = (db.vehicle_records.cameraID>=0)
        lane_condition = (db.vehicle_records.laneNumber>=0)
        direction_condition = (db.vehicle_records.direction>=0)
        license_condition = (db.vehicle_records.license!='_N_A_P_L_V_')
        if 'camera_id' in request.get_vars:
            camera_id = int(request.get_vars['camera_id'])
            camera_condition = (db.vehicle_records.cameraID==camera_id)
        if 'lane_number' in request.get_vars:
            lane_number = int(request.get_var['lane_number'])
            lane_condition = (db.vehicle_records.laneNumber==lane_number)
        if 'direction' in request.get_vars:
            direction = int(request.get_vars['direction'])
            direction_condition = (db.vehicle_records.direction==direction)
        if 'license' in request.get_vars:
            license = request.get_vars['license']
            license_condition = (db.vehicle_records.license.contains(license))
        rs = db( dt_condition & camera_condition & lane_condition & direction_condition & license_condition ).select()
        ret = []
        for rc in rs:
            ret.append(rc.as_dict())
        return json.dumps(dict(status=1, data=ret, error=0, message="Data retrieved."))
    else:
        return json.dumps(dict(status=0, data=[], error=1, message="Error occured while retrieving data."))


