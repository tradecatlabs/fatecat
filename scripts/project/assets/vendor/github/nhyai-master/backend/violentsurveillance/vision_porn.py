#-*- coding: UTF-8 -*-
import sys
import optparse
import time
import apiutils
import base64
import json

app_id = '2117762929'
app_key = '9kXyS3QAsMt9N90m'


def vision_porn(img_file):
    with open(img_file, 'rb') as bin_data:
        image_data = bin_data.read()

    ai_obj = apiutils.AiPlat(app_id, app_key)
    print('----------------------app_id----------------------' + app_id)
    print('----------------------app_key----------------------' + app_key)

    print('----------------------SEND REQ----------------------')
    rsp = ai_obj.getVisionPorn(image_data)

    if rsp['ret'] == 0:
        print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
        print('----------------------API SUCC----------------------')
        return rsp
    else:
        print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
        print('----------------------API FAIL----------------------')
