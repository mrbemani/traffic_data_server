# -*- coding: utf-8 -*-
# syncing data
import json

def new_record():
    if request.method == 'POST':
        reqObj = dict(
            cameraID = int(request.post_vars['cameraID'] or 1),
            laneNumber = int(request.post_vars['laneNumber']),
            direction = int(request.post_vars['direction']),
            checkPointTime = int(request.post_vars['checkPointTime']),
            vehicleClassId = int(request.post_vars['vehicleClassId']),
            speedKmh = round(request.post_vars['speed']),
            plateConfidence = int(request.post_vars['plateConfidence']),
            plateType = request.post_vars['plateType'],
            plateColor = request.post_vars['plateColor'],
            license = request.post_vars['license']
            )
        uniqueID = "T{}C{}L{}D{}".format(reqObj['checkPointTime'], reqObj['cameraID'], reqObj['laneNumber'], reqObj['direction'])
        ret = db.vehicle_records.insert(uniqueID=uniqueID, **reqObj)
        if ret is not None and ret > 0:
            return json.dumps(dict(status=1, error=0, message="Record saved to DB."))
        else:
            return json.dumps(dict(status=0, error=1, message="Record not saved."))
    else:
        raise HTTP(400)
