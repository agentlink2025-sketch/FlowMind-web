# -*- coding:utf-8 -*-
import hashlib
import hmac
import base64
import json
import time
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

class AIPPT():
    def __init__(self, APPId, APISecret, Text, templateId):
        self.APPid = APPId
        self.APISecret = APISecret
        self.text = Text
        self.header = {}
        self.templateId = templateId

    def get_signature(self, ts):
        try:
            auth = self.md5(self.APPid + str(ts))
            return self.hmac_sha1_encrypt(auth, self.APISecret)
        except Exception as e:
            print(e)
            return None

    def hmac_sha1_encrypt(self, encrypt_text, encrypt_key):
        return base64.b64encode(hmac.new(encrypt_key.encode('utf-8'), encrypt_text.encode('utf-8'), hashlib.sha1).digest()).decode('utf-8')

    def md5(self, text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def create_task(self):
        url = 'https://zwapi.xfyun.cn/api/ppt/v2/create'
        timestamp = int(time.time())
        signature = self.get_signature(timestamp)

        formData = MultipartEncoder(
            fields={
                "query": self.text,
                "templateId": self.templateId,
                "author": "MarketManus",
                "isCardNote": str(True),
                "search": str(False),
                "isFigure": str(True),
                "aiImage": "normal"
            }
        )

        headers = {
            "appId": self.APPid,
            "timestamp": str(timestamp),
            "signature": signature,
            "Content-Type": formData.content_type
        }
        self.header = headers

        response = requests.request(method="POST", url=url, data=formData, headers=headers).text
        resp = json.loads(response)
        if resp['code'] == 0:
            return resp['data']['sid']
        else:
            print('创建PPT任务失败')
            return None

    def get_process(self, sid):
        if sid is not None:
            response = requests.request("GET", url=f"https://zwapi.xfyun.cn/api/ppt/v2/progress?sid={sid}", headers=self.header).text
            return response
        return None

    def get_result(self, task_id):
        while True:
            response = self.get_process(task_id)
            resp = json.loads(response)
            pptStatus = resp['data']['pptStatus']
            aiImageStatus = resp['data']['aiImageStatus']
            cardNoteStatus = resp['data']['cardNoteStatus']

            if pptStatus == 'done' and aiImageStatus == 'done' and cardNoteStatus == 'done':
                return resp['data']['pptUrl']
            time.sleep(3) 