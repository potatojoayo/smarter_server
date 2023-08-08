"""한명의 부모가 2명이상의 학생을 데리고 있을때 알람을 하나 보내야하는 상황에서 써먹기"""

from gym_student.models import Student
from notification.models.gym_notification import GymNotification
from notification.models.gym_notification_receiver import GymNotificationReceiver


def gym_notification_method(title, contents, gym, class_masters):
    for class_master in class_masters:
        gym_notification = GymNotification.objects.create(class_master=class_master,
                                                          gym=gym,
                                                          title=title,
                                                          contents=contents,
                                                          )
        students = Student.objects.filter(class_master=class_master,
                                          status="수강중")
        student_list = []
        for student in students:
            student_dic = {
                'parent': student.parent
            }
            exist = False
            for student_object in student_list:
                if student_object['parent'].id == student_dic['parent'].id:
                    exist = True
            if not exist:
                student_list.append(student_dic)

        for student_object in student_list:
            GymNotificationReceiver.objects.create(gym_notification=gym_notification,
                                                   parent=student_object['parent'])
