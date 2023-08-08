from celery import shared_task

from server.celery import app
from src.lib import message
import json

@shared_task
def solapi_async_message(phone_number, random_int):
    print(111111)
    data = {
        'messages': [
            # 변수가 있는 경우
            {
                'to': phone_number,
                'from': '15773754',
                'kakaoOptions': {
                    'pfId': 'KA01PF23042406374863365nYrJl2kke',
                    'templateId': 'KA01TP230427053632026cNBNSx3VG0d',
                    'variables': {
                        '#{code}': str(random_int)
                    }
                }
            }
        ]
    }
    message.send_many(data)
    # print(json.dumps(res.json(), indent=2, ensure_ascii=False))
