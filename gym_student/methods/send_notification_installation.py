from celery import shared_task

from business.models import Gym
from src.lib import message


@shared_task
def send_notification_installation(phone_number, gym_id):
    gym = Gym.objects.get(pk=gym_id)
    gym_name = gym.name
    data = {
        'messages': [
            # 변수가 있는 경우
            {
                'to': phone_number,
                'from': '15773754',
                'kakaoOptions': {
                    'pfId': 'KA01PF23042406374863365nYrJl2kke',
                    'templateId': 'KA01TP230504025821139Gdgrwt4cKhB',
                    'variables': {
                        '#{gym_name}': gym_name
                    }
                }
            },
        ]
    }
    message.send_many(data)
    data_1 = {
        'messages':[
            {
                'to': phone_number,
                'from': '15773754',
                'kakaoOptions': {
                    'pfId': 'KA01PF23042406374863365nYrJl2kke',
                    'templateId': 'KA01TP230509080455241ohZlOmVsQDv',
                    'variables': {}  # 변수가 없는 경우에도 입력
                }
            }
        ]
    }
    message.send_many(data_1)