# -*- coding: utf-8 -*-
# syncing data
import json
import time
import os

def new_record():
    if request.method == 'POST':
        cameraUID = request.post_vars['cameraUID']
        is_camera_rcid = bool(int(request.post_vars['is_camera_rcid'] or '0'))
        reqObj = dict(
            laneNumber = int(request.post_vars['laneNumber']),
            direction = int(request.post_vars['direction']),
            checkPointTime = int(request.post_vars['checkPointTime']),
            vehicleClassId = int(request.post_vars['vehicleClassId']),
            speedKmh = round(float(request.post_vars['speed'])),
            plateConfidence = int(request.post_vars['plateConfidence']),
            plateType = request.post_vars['plateType'],
            plateColor = request.post_vars['plateColor'],
            license = request.post_vars['license']
        )
        ckpt_minisec = reqObj["checkPointTime"]
        if reqObj["checkPointTime"] > 9999999999:
            reqObj['checkPointTime'] = int(reqObj['checkPointTime'] / 1000)
        cameraID = 0
        if is_camera_rcid:
            cameraID = int(cameraUID)
        else:
            rc_camera = db(db.camera.uniqueID == cameraUID).select().first()
            if rc_camera is None:
                return json.dumps(dict(status=0, data=None, error=3, message="Invalid cameraUID"))
            cameraID = rc_camera._id
            # poleID = rc_camera.poleID
            # tunnelID = rc_camera.poleID.tunnelID
        uniqueID = "TM{}C{}L{}D{}".format(ckpt_minisec, cameraID, reqObj['laneNumber'], reqObj['direction'])
        ret = db.vehicle_records.insert(uniqueID=uniqueID, cameraID, **reqObj)
        if ret is not None and ret > 0:
            return json.dumps(dict(status=1, data=dict(record_id=ret), error=0, message="Record saved to DB."))
        else:
            return json.dumps(dict(status=0, data=None, error=1, message="Record not saved."))
    else:
        raise HTTP(400)


def add_photo(): # just pasted from ddw, to be fixed....
    ret = json.dumps(dict(status=0, data=None, error=-1, message="unknown error"))
    rcid = 0
    #if True:
    try:
        rcid = int(request.get_vars['rcid'])
        if rcid < 1:
            raise Exception("rcid parameter is invalid")
        ftype = str(request.post_vars.upfile.type)
        ext = 'jpg'
        if ftype.lower().endswith('/png'):
            ext = 'png'
        elif ftype.lower().endswith('/gif'):
            ext = 'gif'
        new_name = "VEHICLE_{}_{}.{}".format(rcid, int(time.time()*1000), ext)
        image_data = request.post_vars.upfile.file.read()
        new_image_file_path = os.path.join(os.path.abspath('.'), "applications", request.application, "static", "capture", "vehicles", new_name)
        fp = open(new_image_file_path, 'w+b')
        fp.write(image_data)
        fp.close()
        photodata = dict(
            name=new_name,
            url="{}/{}".format(PHOTO_URL_PREFIX, new_name),
            size=len(image_data),
            ftype=ftype
        )
        phid = db.photo.insert(name=photodata['name'], record_id=rcid)
        if phid > 0:
            photodata['photo_record_id'] = phid
            info = dict(
                data=photodata,
                error=0,
                message="photo uploaded",
                status=1
            )
        else:
            info = dict(
                status=0, 
                error=2, 
                message="Failed to write image record into DB.",
                data=None
            )
        ret = json.dumps(info)
    except Exception as e:
        info = dict(
            status=0, 
            error=1, 
            message=repr(e),
            data=None
        )
        ret = json.dumps(info)
    finally:
        return ret