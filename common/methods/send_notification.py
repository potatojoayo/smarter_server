from django.contrib.auth.models import Group

from authentication.models import User
from common.methods.create_notification import create_notification
from common.methods.get_bank_infos import get_bank_infos
from common.models import BankAccount
from order.models import OrderDetail


def send_notification(user=None,
                      type=None,
                      product_names=None,
                      quantity=None,
                      order_master=None,
                      amount=None,
                      subcontractor=None,
                      order_name=None,
                      coupon_master=None,
                      issue_coupon_number=None, coupon_message=None):
    delivery = Group.objects.get(name="배송관리팀")
    delivery_users = User.objects.filter(groups=delivery)
    admin = Group.objects.get(name="관리자")
    admin_users = User.objects.filter(groups=admin)
    gym_name = user.gym.name
    draft = Group.objects.get(name="로고시안팀")
    draft_users = User.objects.filter(groups=draft)
    bank_account = BankAccount.objects.get(is_default=True)

    if type == "무통장입금안내":
        bank_infos = get_bank_infos()
        title = '무통장입금안내'
        contents = '요청하신 스마터머니 {:0,.0f}원 충전을 완료하시려면 {}으로 {:0,.0f}원을 입금해주세요.' \
            .format(amount, bank_infos, amount)
        create_notification.delay(notification_type=title, title=title, contents=contents, user_id=user.id)

    elif type == "간편주문 결제요청":
        create_notification.delay(user_id=user.id, notification_type="간편주문 결제요청", title="간편주문 결제요청",
                            contents="알림을 눌러 {} 상품 주문의 결제를 진행해주세요."
                            .format(product_names),
                            route='/order/{}'.format(order_master.id))
    elif type == "배송중":
        if len(product_names) == 1:
            create_notification.delay(user_id=user.id, title='배송중', notification_type='배송중',
                                contents='{}의 {}상품이 배송중입니다.'
                                .format(user.name, product_names[0]))
        else:
            create_notification.delay(user_id=user.id, title='배송중', notification_type='배송중',
                                contents='{}의 {}외 {}건의 상품이 배송중입니다.'
                                .format(user.name, product_names[0], len(product_names) - 1))
    elif type == "묶음배송중":
        products = list(set(product_names))
        create_notification.delay(user_id=user.id, title="배송중",
                            contents="주문하신 {} 상품을 한꺼번에 보내드리겠습니다, 쓰이지 않은 배송비 {}원은 스마터 머니로 적립되었습니다."
                            .format(', '.join(products), amount),
                            notification_type='배송중')
    elif type == "쿠폰발급":
        create_notification.delay(user_id=user.id, title="쿠폰발급",
                                  contents="{}".format(coupon_message if coupon_message else coupon_master.coupon_message, issue_coupon_number),
                                  notification_type="쿠폰발급")
    """
    if type == "추후배송":
        create_notification(user=user, title="배송지연",
                            contents="{}의 수량부족으로 배송이 지연되었습니다. 수량 확보시 곧바로 배송하겠습니다.".format(
                                product_names), notification_type="배송지연")
        for delivery_user in delivery_users:
            create_notification(user=delivery_user, title="추후배송요청",
                                contents="{}에서 주문한 {}상품의 재고가 부족하여 추후배송상태로 변경되었습니다.".format(gym_name,
                                                                                            product_names),
                                notification_type='추후배송요청')
    elif type == '취소완료':
        create_notification(user=user, title="취소완료",
                            contents="{}의 {}  주문이 취소되었습니다.".format(gym_name, product_names),
                            notification_type="취소완료")
        for admin_user in admin_users:
            create_notification(user=admin_user, title='취소완료',
                                contents='{}의 {} 주문이 취소되었습니다.'.format(gym_name, product_names),
                                notification_type='취소완료')
    elif type == "묶음배송":
        if quantity == 1:
            create_notification(user=user, title="출고준비",
                                contents="주문하신 {} 상품이 출고준비중입니다."
                                .format(product_names),
                                notification_type='출고준비')
            for delivery_user in delivery_users:
                create_notification(user=delivery_user, title="묶음배송",
                                    contents="{}에서 묶음배송을 요청하였습니다.".format(gym_name),
                                    notification_type='묶음배송')
        else:
            create_notification(user=user, title="출고준비",
                                contents="주문하신 {} 상품 외 {}개가 출고준비중입니다."
                                .format(product_names, quantity-1),
                                notification_type='출고준비')
            for delivery_user in delivery_users:
                create_notification(user=delivery_user, title="묶음배송",
                                    contents="{}에서 {} 상품 외 {}개를 묶음배송을 요청하였습니다.".format(gym_name, product_names,
                                                                                       quantity-1),
                                    notification_type='묶음배송')

    elif type == "출고준비":
        if quantity == 1:
            create_notification(user=user, title="출고준비",
                                contents="주문하신 {} 상품이 출고준비중입니다."
                                .format(product_names),
                                notification_type='출고준비')
            for delivery_user in delivery_users:
                create_notification(user=delivery_user, title="출고준비",
                                    contents="{}의 상품이 출고준비중입니다.".format(gym_name),
                                    notification_type='출고준비')
        else:
            create_notification(user=user, title="출고준비",
                                contents="주문하신 {} 상품 외 {}개가 출고준비중입니다."
                                .format(product_names, quantity-1),
                                notification_type='출고준비')
            for delivery_user in delivery_users:
                create_notification(user=delivery_user, title="출고준비",
                                    contents="{}의 {}상품 외 {}개가 출고준비중입니다.".format(gym_name, product_names, quantity-1),
                                    notification_type='출고준비')
    elif type == '간편주문요청':
        create_notification(user=user, title="간편주문완료",
                            contents="간편주문을 요청하였습니다. 확인 후 연락드리겠습니다"
                            .format(user.name),
                            notification_type="간편주문완료")
        for admin_user in admin_users:
            create_notification(user=admin_user, title="간편주문",
                                contents="{}님께서 간편주문을 요청하였습니다."
                                .format(user.name),
                                notification_type="간편주문")
    elif type == "교환요청":
        create_notification(user=user, contents='{} 상품 {}개를 교환요청 하였습니다.'
                            .format(product_names, quantity),
                            notification_type='교환요청',
                            title='교환요청'
                            )
        for admin_user in admin_users:
            create_notification(user=admin_user, title="교환요청",
                                contents="{}님께서 {}상품을 교환 요청하였습니다."
                                .format(user.name, product_names),
                                notification_type="교환요청")
    elif type == "반품요청":
        create_notification(user=user, contents='{} 상품 {}개를 반품요청 하였습니다.'
                            .format(product_names, quantity),
                            notification_type='교환요청',
                            title='교환요청'
                            )
        for admin_user in admin_users:
            create_notification(user=admin_user, title="반품요청",
                                contents="{}님께서 {}을 반품 요청하였습니다."
                                .format(user.name, product_names),
                                notification_type="반품요청")
    elif type == "재고부족":
        for admin_user in admin_users:
            create_notification(user=admin_user, title="재고부족",
                                contents="{}이 재고가 부족합니다. 발주요청 드립니다."
                                .format(product_names),
                                notification_type="재고부족")
    elif type == "후작업완료":
        create_notification(user=user, notification_type="후작업완료",
                            title="후작업완료",
                            contents="주문하신 {}의 후작업이 완료되었습니다.".format(product_names))
        for admin_user in admin_users:
            create_notification(user=admin_user, notification_type="작업완료",
                                title="작업완료",
                                contents="{}님께서 주문하신 {}의 후작업이 완료되었습니다.".format(user.name,
                                                                               product_names))
    elif type == "시안요청":
        create_notification(user=user,
                            notification_type='시안요청',
                            title='시안요청',
                            contents='{} 상품의 로고시안을 요청하였습니다.'.format(product_names)
                            )
        for draft_user in draft_users:
            create_notification(user=draft_user,
                                notification_type='시안요청',
                                title='시안요청',
                                contents='{}에서 {} 상품의 로고시안을 요청하셨습니다.'.format(gym_name, product_names)
                                )
    elif type == "시안완료":
        create_notification(user=user, title='시안완료', notification_type='시안완료',
                            contents='{}상품의 시안이 완료되었습니다. 주문을 진행해주시기 바랍니다.'.format(product_names))
    """
    """
    elif type == "교환완료":
        create_notification(user=user, notification_type="교환완료", title="교환완료",
                            contents="{}상품 {}개를 교환완료 하였습니다.".format(product_names, quantity))
    elif type == "반품완료":
        create_notification(user=user, notification_type="반품완료", title="반품완료",
                            contents="{}상품 {}개를 반품완료 하였습니다.".format(product_names, quantity))
    elif type == "교환반려":
        create_notification(user=user, notification_type="교환반려", title="교환반려",
                            contents="{}상품 {}개가 교환반려 되었습니다.".format(product_names, quantity))
    elif type == "반품반려":
        create_notification(user=user, notification_type="반품반려", title="반품반려",
                            contents="{}상품 {}개가 반품반려 되었습니다.".format(product_names, quantity))
    elif type == "주문확인":
        bank_info = get_bank_infos()
        product_master_numbers = OrderDetail.objects.filter(order_master=order_master).count()
        if product_master_numbers == 1:
            create_notification(user=user, notification_type='주문확인', title="입금요청",
                                contents='{}의 주문을 완료하시려면 {}으로 {:0.0f}원을 입금해주세요.'
                                .format(order_master.order_name, bank_info, order_master.price_to_pay))
        else:
            create_notification(user=user,
                                notification_type='주문확인',
                                title='입금요청',
                                contents='{} 외 {}건의 주문을 완료하시려면 {}으로 {:0,.0f}원을 입금해주세요.'
                                .format(order_master.order_name, product_master_numbers-1, bank_info,
                                        order_master.price_to_pay))
    
    """
    """
    elif type == "충전":
        create_notification(notification_type='충전',
                            title="충전",
                            contents="스마터머니 {:0,.0f}원이 충전되었습니다.".format(amount),
                            user=user,
                            route='/smarter-money'
                            )
    elif type == "취소요청":
        create_notification(user=user, title='취소요청',
                            contents='{}의 {} 주문에 대한 취소 요청이 접수되었습니다.'.format(gym_name, product_names),
                            notification_type='취소요청',
                            )
        for admin_user in admin_users:
            create_notification(user=admin_user, title='취소요청',
                                contents='{}의 {} 주문에 대한 취소 요청이 접수되었습니다.'.format(gym_name, product_names),
                                notification_type='취소요청',
                                )
    elif type == "취소완료":
        create_notification(user=user, title='취소완료',
                            contents='{}의 {} 주문에 대한 취소가 완료되었습니다.'.format(gym_name, product_names),
                            notification_type='취소완료',
                            )
    elif type == "결제완료":
        create_notification(user=user,
                            notification_type='결제완료',
                            title='결제완료',
                            contents='{}의 주문이 완료되었어요. 필요한 후작업이 있다면 진행 후 고객님께 상품을 보내드리겠습니다.'
                            .format(order_master.order_name))
    elif type == "작업실배정":
        create_notification(user=subcontractor.user, notification_type="작업실배정",
                            title="작업실배정",
                            contents="{}님의 상품이 {}에 배정되었습니다.".format(user.name, subcontractor.name))
    elif type == "후작업중":
        # 작업실에 알람
        create_notification(user=subcontractor.user, title="후작업중", notification_type="후작업중",
                            contents="{}님께서 주문하신 {}이 {}에 배정되었습니다.".format(user.name,
                                                                          order_name,
                                                                          subcontractor.name))
        # 사용자에게 알람
        create_notification(user=user, title="후작업중", notification_type="후작업중",
                            contents="주문하신 {}의 후작업중입니다".format(order_name))
    
    elif type == '회원가입승인':
        create_notification(user=user, title="회원가입 승인",
                            contents="회원가입이 승인되었습니다.",
                            notification_type='회원가입승인')
    """
