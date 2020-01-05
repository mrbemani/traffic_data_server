# -*- coding: utf-8 -*-
# traffic data

import json


def get_camera_by_uid():
    ret = json.dumps(dict(status=0, data=[], error=-1, message="Unknown error."))
    if len(request.args) < 1:
        return json.dumps(dict(status=0, data=None, error=1, message="No cameraUID presented."))
    camera_uid = request.args[0]
    return camera_rcid


def get_camera_by_id():
    ret = json.dumps(dict(status=0, data=[], error=-1, message="Unknown error."))
    if len(request.args) < 1:
        return json.dumps(dict(status=0, data=None, error=1, message="No cameraID presented."))
    camera_rcid = int(request.args[0])
    camera_rc = db.camera[camera_rcid]
    if camera_rc is None:
        return json.dumps(dict(status=0, data=None, error=2, message="Invalid cameraID."))
    return json.dumps(dict(status=1, data=camera_rc.as_dict(), error=0, message="Camera retrieved."))


def get_cameras_by_pole_id():
    ret = json.dumps(dict(status=0, data=[], error=-1, message="Unknown error."))
    if len(request.args) < 1:
        return json.dumps(dict(status=0, data=None, error=1, message="No poleID presented."))
    pole_rcid = int(request.args[0])
    cameras_on_pole = db(db.camera.poleID == pole_rcid).select()
    ret_cameras = []
    for c in cameras_on_pole:
        ret_cameras.append(c.as_dict())
    return json.dumps(dict(status=1, data=ret_cameras, error=0, message="Camera list retrieved."))


def get_poles_by_tunnel_id():
    ret = json.dumps(dict(status=0, data=[], error=-1, message="Unknown error."))
    if len(request.args) < 1:
        return json.dumps(dict(status=0, data=None, error=1, message="No poleID presented."))
    pole_rcid = int(request.args[0])
    cameras_on_pole = db(db.camera.poleID == pole_rcid).select()
    ret_cameras = []
    for c in cameras_on_pole:
        ret_cameras.append(c.as_dict())
    return json.dumps(dict(status=1, data=ret_cameras, error=0, message="Camera list retrieved."))

