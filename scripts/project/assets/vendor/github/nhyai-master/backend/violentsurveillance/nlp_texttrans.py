#-*- coding: UTF-8 -*-
import sys
import optparse
import time
import apiutils
import json

app_id = '2117762929'
app_key = '9kXyS3QAsMt9N90m'

if __name__ == '__main__':
    str_text = '今天天气怎么样'
    type = 1
    ai_obj = apiutils.AiPlat(app_id, app_key)

    print('----------------------SEND REQ----------------------')
    rsp = ai_obj.getNlpTextTrans(str_text, type)
    if rsp['ret'] == 0:
        print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
        print('----------------------API SUCC----------------------')
    else:
        print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
        # print rsp
        print('----------------------API FAIL----------------------')

