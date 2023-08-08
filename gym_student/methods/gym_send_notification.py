from common.methods.create_notification import create_notification


def gym_send_notification(user=None, type=None, audition_master=None,
                          date_absent=None, attendance_hour=None, attendance_min=None,
                          gym_notification_title=None, audition_detail=None, date_to_pay=None,
                          date_absent_end = None):
    if type == "학생승급일 15일전 알림":
        create_notification.delay(user_id=user.parent.user.id, title='승급일', notification_type=type,
                            contents="{}의 {} 승급일이 15일 남았습니다."
                            .format(user.name, audition_master.next_level.name))
    elif type == "체육관승급일 15일전 알림":
        create_notification.delay(user_id=user.id, title='승급일', notification_type=type,
                                contents="{} 승급일이 15일 남았습니다".format(audition_master.next_level))
    elif type == "학생승급일 7일전 알림":
        create_notification.delay(user_id=user.parent.user.id, title='승급일', notification_type=type,
                            contents="{}의 {} 승급일이 7일 남았습니다."
                            .format(user.name, audition_master.next_level.name)
                            )
    elif type == "학생승급심사일 알림":
        create_notification.delay(user_id=user.parent.user.id, title='승급심사일', notification_type=type,
                            contents="{}의 {} 승급심사일은 {}입니다. 감사합니다"
                            .format(user.name, audition_master.next_level.name, audition_master.estimated_alarm_date[:10]))
    elif type == "체육관승급일 7일전 알림":
        create_notification.delay(user_id=user.id, title='승급일', notification_type=type,
                                contents="{} 승급일이 7일 남았습니다".format(audition_master.next_level))
    elif type == "결석예정 알림":
        if date_absent == date_absent_end:
            create_notification.delay(user_id=user.class_master.gym.user.id, title='결석예정', notification_type=type,
                                contents="{}의 {}학생이 {} 에 결석을 신청 하였습니다. 앱캘린더를 확인하여 주시기 바랍니다 "
                                .format(user.class_master.name, user.name, date_absent.strftime('%Y-%m-%d')))
            create_notification.delay(user_id=user.parent.id, title='결석예정', notification_type=type,
                                      contents="{}의 {}학생이 {} 에 결석을 신청 하였습니다. 앱캘린더를 확인하여 주시기 바랍니다 "
                                      .format(user.class_master.name, user.name, date_absent.strftime('%Y-%m-%d')))
        else:
            create_notification.delay(user_id=user.class_master.gym.user.id, title='결석예정', notification_type=type,
                                contents="{}의 {}학생이 {} - {} 에 결석을 신청 하였습니다. 앱캘린더를 확인하여 주시기 바랍니다 "
                                .format(user.class_master.name, user.name,
                                        date_absent.strftime('%Y-%m-%d'), date_absent_end.strftime('%Y-%m-%d')))
            create_notification.delay(user_id=user.parent.id, title='결석예정', notification_type=type,
                                      contents="{}의 {}학생이 {} - {} 에 결석을 신청 하였습니다. 앱캘린더를 확인하여 주시기 바랍니다 "
                                      .format(user.class_master.name, user.name,
                                              date_absent.strftime('%Y-%m-%d'), date_absent_end.strftime('%Y-%m-%d')))
    elif type == "등원알림":
        create_notification.delay(user_id=user.parent.user.id, title='등원', notification_type=type,
                            contents="{} {} {}시 {}분에 등원하였습니다. 감사합니다 "
                            .format(user.class_master.name, user.name, attendance_hour, attendance_min))

    elif type == "하원알림":
        create_notification.delay(user_id=user.parent.user.id, title='하원', notification_type=type,
                            contents="{} 수업아 종료되었습니다. 감사합니다"
                            .format(user.class_master.name, user.name, attendance_hour, attendance_min))
    elif type == "결석알림":
        create_notification.delay(user_id=user.parent.user.id, title='결석', notification_type=type,
                            contents="{} {} 등원하지 않았습니다. 부모님께 확인 부탁드립니다."
                            .format(user.class_master, user.name, attendance_hour, attendance_min))
    elif type == "알림장알림":
        create_notification.delay(user_id=user.parent.user.id, title='알림장', notification_type=type,
                            contents="{}".format(gym_notification_title),)
    elif type == "학원비 청구서 발급":
        create_notification.delay(user_id=user.parent.user.id, title='학원비', notification_type=type,
                            contents="{} {}의 이번달 학원비 청구서가 발급되었습니다. 앱에서 비대면 카드결제 서비스도 제공하여 드립니다. 감사합니다"
                            .format(user.class_master, user.name))
    elif type == "학원비 수금일 알림":
        create_notification.delay(user_id=user.parent.user.id, title='학원비', notification_type=type,
                            contents="오늘은 {} {}의 이번달 학원비 납부일입니다. "
                            .format(user.class_master.name, user.name))
    elif type == "학원비 알림":
        create_notification.delay(user_id=user.parent.user.id, title='학원비', notification_type=type,
                            contents="{} {}의 미납된 학원비를 수납하여 주시길 바랍니다. 혹시 오류가 있는 경우 연락 부탁 드립니다. 감사합니다 "
                            .format(user.class_master.name, user.name))
    elif type == "승급 완료 알림":
        create_notification.delay(user_id=user.id, title='승급 완료', notification_type=type,
                            contents="{}의 {} 승급이 합격 되었습니다. 부모님 수고하셨습니다.".format(audition_detail.student.name, audition_detail.audition_master.next_level.name))
    elif type == "승급 실패 알림":
        create_notification.delay(user_id=user.id, title='승급 실패', notification_type=type,
                            contents="{}의 {} 승급이 아쉽게 실패 하였습니다. 다음엔 꼭 합격될것입니다. 감사합니다.".format(audition_detail.student.name, audition_detail.audition_master.next_level.name))
