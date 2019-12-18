# -*- coding: utf-8 -*-
# syncing data
import json

def new_record():
    if request.method == 'POST':
        request.post_vars['passtime']
        return json.dumps(request.post_vars)
    else:
        raise HTTP(400)
