# -*- coding: utf-8 -*-
# syncing data
import json
import time
import os

def new_record():
    if request.method == 'POST':
        reqObj = dict(
            cameraID = int(request.post_vars['cameraID'] or 1),
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
        uniqueID = "T{}C{}L{}D{}".format(reqObj['checkPointTime'], reqObj['cameraID'], reqObj['laneNumber'], reqObj['direction'])
        ret = db.vehicle_records.insert(uniqueID=uniqueID, **reqObj)
        if ret is not None and ret > 0:
            return json.dumps(dict(status=1, data=None, error=0, message="Record saved to DB."))
        else:
            return json.dumps(dict(status=0, data=None, error=1, message="Record not saved."))
    else:
        raise HTTP(400)


def add_photo(): # just pasted from ddw, to be fixed....
    ret = json.dumps(dict(ok=False))
    m_code = ""
    m_mac = ""
    try:
        #orgName = str(request.post_vars.upfile.filename)
        m_code = request.post_vars.code
        m_mac = request.post_vars.mac
        ftype = str(request.post_vars.upfile.type)
        ext = 'jpg'
        if ftype.lower().endswith('/png'):
            ext = 'png'
        elif ftype.lower().endswith('/gif'):
            ext = 'gif'
        new_name = "VEHICLE_{}.{}".format(int(time.time()*1000), ext)
        image_data = str(request.post_vars.upfile.file.read())
        new_image_file_path = os.path.join(os.path.abspath('.'), "applications", request.application, "static/photos", new_name)
        watermark_file_path = os.path.join(os.path.abspath('.'), "applications", request.application, "static/images/photo_overlay.png")
        fp = open(new_image_file_path, 'w+b')
        fp.write(image_data)
        fp.close()
        im_bg = Image.open(new_image_file_path)
        im_fg = Image.open(watermark_file_path)
        fgsize = im_fg.size
        bgsize = im_bg.size
        nw = bgsize[0]
        nh = int(float(fgsize[1]) / float(fgsize[0]) * float(nw))
        im_fg = im_fg.resize((nw, nh), Image.BICUBIC)
        im_bg.paste(im_fg, (0, 0), im_fg)
        im_bg.save(new_image_file_path)
        info = dict(
            name=new_name,
            url=URL('static', 'photos', args=(new_name,)), #$this->fullName,
            size=len(image_data), #$this->fileSize,
            ftype=ftype, #$this->fileType,
            ok=True
        )

        if db(db.photo.code == m_code).count() == 0:
            db.photo.insert(url=info['url'], code=m_code, mac=m_mac)
        else:
            db(db.photo.code == m_code).update(url=info['url'])
        ret = json.dumps(info)
    except Exception as e:
        info = dict(
            error=e,
            ok=False
        )
        ret = json.dumps(info)
    finally:
        # reset machine
        m_code = gen_control_code(m_mac)
        m_state = 0
        m_job = ''
        db(db.machine.id == 1).update(mach_state=m_state, control_code=m_code, control_start=0, job=m_job)
        ###
        return ret