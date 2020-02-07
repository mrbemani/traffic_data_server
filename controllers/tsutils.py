# -*- coding: utf-8 -*-
# traffic data

import os
import shutil
from PIL import Image

def tsu_rearrange_snapshots():
    startidx = 0
    maxlen = 100
    outtext = ""
    if "idx" in request.get_vars:
        startidx = int(request.get_vars["idx"])
    capdir = os.path.join(os.path.abspath('.'), "applications", request.application, "static", "capture")
    rs = db(db.vehicle_records._id>startidx).select(db.vehicle_records.ALL, limitby=(0, maxlen))
    last_id = startidx
    for itm in rs:
        ph = db(db.photo.record_id==itm.id).select().first()
        if ph is not None:
            fin = os.path.join(capdir, "vehicles", ph.name)
            vehclsdir = os.path.join(capdir, str(itm.vehicleClassId))
            if os.path.exists(vehclsdir):
                if not os.path.isdir(vehclsdir):
                    os.unlink(vehclsdir)
                    os.mkdir(vehclsdir)
            else:
                os.mkdir(vehclsdir)
            fout = os.path.join(vehclsdir, ph.name)
            shutil.copy(fin, fout)
            outtext += "[{}] {} => {} \r\n".format(itm.id, fin, fout)
        last_id = itm.id
    return dict(outtext=outtext, idx=last_id)


def tsu_generate_thumbnails():
    startidx = 0
    maxlen = 1000
    outtext = ""
    if "idx" in request.get_vars:
        startidx = int(request.get_vars["idx"])
    capdir = os.path.join(os.path.abspath('.'), "applications", request.application, "static", "capture", "vehicles")
    rs = db(db.photo._id>startidx).select(db.photo.ALL, limitby=(0, maxlen))
    last_id = startidx
    thumbsize = (60, 60)
    thumbs_dir = os.path.join(capdir, "thumbs")
    for ph in rs:
        fin = os.path.join(capdir, ph.name)
        ph_name = ph.name.split('.')
        ph_new_name = ".".join([*ph_name[:-1], "thumb_60x60", ph_name[-1]])
        fout = os.path.join(thumbs_dir, ph_new_name)
        if os.path.exists(thumbs_dir):
            if not os.path.isdir(thumbs_dir):
                os.unlink(thumbs_dir)
                os.mkdir(thumbs_dir)
        else:
            os.mkdir(thumbs_dir)
        im = Image.open(fin)
        im.thumbnail(thumbsize)
        im.save(fout, "JPEG")
        outtext += "[{}] {}... \r\n".format(ph.id, fin)
        last_id = ph.id
        db.mytable[ph.id] = dict(thumbnail="thumbs/{}".format(ph_new_name))
    return dict(outtext=outtext, idx=last_id)

    