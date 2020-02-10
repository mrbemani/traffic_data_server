# -*- coding: utf-8 -*-
# syncing data
import json
import time
import os
from PIL import Image

def new_record():
    if request.method == 'POST':
        cameraUID = request.post_vars['cameraUID']
        reqObj = dict(
            laneNumber = int(request.post_vars['laneNumber']),
            direction = int(request.post_vars['direction']),
            checkPointTime = int(request.post_vars['checkPointTime']),
            vehicleClassConfidence = int(request.post_vars['vehicleClassConfidence']),
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
        uniqueID = "TM{}C{}L{}D{}".format(ckpt_minisec, cameraUID, reqObj['laneNumber'], reqObj['direction'])
        ret = db.vehicle_records.insert(uniqueID=uniqueID, cameraUID=cameraUID, **reqObj)
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
        new_name_prefix = "VEHICLE_{}_{}".format(rcid, int(time.time()*1000))
        new_name = new_name_prefix + "." + ext
        image_data = request.post_vars.upfile.file.read()
        capdir = os.path.join(os.path.abspath('.'), "applications", request.application, "static", "capture", "vehicles")
        new_image_file_path = os.path.join(capdir, new_name)
        fp = open(new_image_file_path, 'w+b')
        fp.write(image_data)
        fp.close()
        # write thumbnail
        thumbsize = (60, 60)
        thumbs_dir = os.path.join(capdir, "thumbs")
        ph_thumb_name = new_name_prefix + ".thumb_60x60." + ext
        fout = os.path.join(thumbs_dir, ph_thumb_name)
        im = Image.open(new_image_file_path)
        im.thumbnail(thumbsize)
        im.save(fout, "JPEG")
        photodata = dict(
            name=new_name,
            thumbnail="thumbs/{}".format(ph_thumb_name),
            url="{}/{}".format(PHOTO_URL_PREFIX, new_name),
            size=len(image_data),
            ftype=ftype
        )
        phid = db.photo.insert(name=photodata['name'], thumbnail=photodata['thumbnail'], record_id=rcid)
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


def update_equipment_runtime():
    if "gid" not in request.get_vars:
        raise HTTP(400)
        return
    gid = int(request.get_vars['gid'])
    data_json = request.body.read()
    if gid <= 0 or len(data_json) < 1:
        raise HTTP(400)
        return
    import sys
    try:
        db_ret = db.executesql("UPDATE equipment_runtime SET data_json=%s WHERE gid=%s;", (data_json, gid))
        return data_json
    except:
        return sys.exc_info()[1]