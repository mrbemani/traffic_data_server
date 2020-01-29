# -*- coding: utf-8 -*-
# traffic data

import os
import shutil

def tsu_rearrange_snapshots():
    startidx = 0
    maxlen = 100
    outtext = ""
    if "idx" in request.get_vars:
        startidx = request.get_vars["idx"]
    capdir = os.path.join(os.path.abspath('.'), "applications", request.application, "static", "capture")
    rs = db(db.vehicle_records._id>startidx).select(db.vehicle_records.ALL, limitby=(startidx, startidx+maxlen))
    for itm in rs:
        ph = db(db.photo.record_id==itm._id).select().first()
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
            outtext += "<p>{} => {}</p>\r\n".format(fin, fout)
        startidx += 1
    return dict(outtext=outtext, idx=startidx)


    