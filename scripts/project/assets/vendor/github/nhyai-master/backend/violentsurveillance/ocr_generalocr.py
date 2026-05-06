#-*- coding: UTF-8 -*-
import sys
import optparse
import time
import apiutils
import base64
import json

app_id = '2117762929'
app_key = '9kXyS3QAsMt9N90m'

if __name__ == '__main__':
    with open('./data/generalocr.jpg', 'rb') as bin_data:
        image_data = bin_data.read()

    ai_obj = apiutils.AiPlat(app_id, app_key)
    print('----------------------app_id----------------------' +app_id)
    print('----------------------app_key----------------------' + app_key)

    print('----------------------SEND REQ----------------------')
    rsp = ai_obj.getOcrGeneralocr(image_data)

    if rsp['ret'] == 0:
        for i in rsp['data']['item_list']:
            print(i['itemstring'])
        print('----------------------API SUCC----------------------')
    else:
        print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
        print('----------------------API FAIL----------------------')
