from datetime import datetime, date

import graphene
from django.core.exceptions import ObjectDoesNotExist

from business.models import Gym
from gym_class.models import Level, ClassMaster, AttendanceDetail, AttendanceMaster, AbsentRequest
from gym_class.types import ClassMasterType
from gym_class.types.absent_request_type import AbsentRequestType
from gym_student.fields.audition_master_field import AuditionMasterField
from gym_student.fields.my_children_audition_field import MyChildrenAuditionField
from gym_student.models import Student, School, AuditionMaster, AuditionDetail, Parent, Relationship
from gym_student.fields.student_field import StudentField
from gym_student.models import School, Student
from gym_student.mutations.attendance_for_all_classes import AttendanceForAllClasses
from gym_student.mutations.attendance_for_student import AttendanceForStudent
from gym_student.mutations.audition.add_audition_detail import AddAuditionDetail
from gym_student.mutations.audition.audition_detail_pass import AuditionDetailPass
from gym_student.mutations.audition.audition_master_pass import AuditionMasterPass
from gym_student.mutations.audition.create_audition import CreateAudition
from gym_student.mutations.audition.delete_audition_detail import DeleteAuditionDetail
from gym_student.mutations.audition.delete_audition_master import DeleteAuditionMaster
from gym_student.mutations.parent.update_parent import UpdateParent
from gym_student.mutations.student.create_student import CreateStudent
from gym_student.mutations.student.delete_student import DeleteStudent
from gym_student.mutations.student.other_class_attendance import OtherClassAttendance
from gym_student.mutations.student.student_attendance import StudentAttendance
from gym_student.mutations.student.update_students import UpdateStudents
from graphene import relay

from gym_student.types.audition_master.audition_master_node import AuditionMasterNode
from gym_student.types.parent_type import ParentType
from gym_student.types.relationship_type import RelationshipType
from gym_student.types.schedule_for_parent_type import ScheduleForParentType
from gym_student.types.school_type import SchoolType
from gym_student.types.student_statistic_type import StudentStatisticType
from gym_student.types.studnet_node import StudentNode

from gym_student.types.audition_detail.audition_detail_connection import AuditionDetailConnection
from gym_student.types.audition_master.audition_master_connection import AuditionMasterConnection
from gym_student.types.student.student_connection import StudentConnection
from gym_student.types.student.student_type import StudentType
from gym_student.types.parent_type import ParentType
from gym_student.types.school_type import SchoolType
from gym_student.types.studnet_node import StudentNode


class Query(graphene.ObjectType):
    all_students = graphene.List(StudentType)
    students = relay.ConnectionField(StudentConnection,
                                     class_master_id=graphene.Int(),
                                     level_id=graphene.Int(),
                                     school_id=graphene.Int())
    student = graphene.Field(StudentType, id=graphene.Int())
    audition_master = relay.Node.Field(AuditionMasterNode)
    audition_detail = relay.ConnectionField(AuditionDetailConnection, audition_master_id=graphene.Int())
    students_by_parent = graphene.List(StudentType)
    my_students = StudentField(StudentNode)
    my_children = graphene.List(StudentType)
    my_schools = graphene.List(SchoolType)
    my_auditions = AuditionMasterField(AuditionMasterNode, year=graphene.Int(), month=graphene.Int())
    my_children_auditions = MyChildrenAuditionField(AuditionMasterNode, year=graphene.Int(), month=graphene.Int())
    parent = graphene.Field(ParentType, phone=graphene.String())
    relationships = graphene.List(RelationshipType)
    student_schedule_for_parent = graphene.Field(ScheduleForParentType, date=graphene.Date())
    student_statistics = graphene.List(StudentStatisticType, class_master_name=graphene.String(), year=graphene.Int())
    students_by_code = graphene.List(StudentType, code=graphene.String())
    gym_absent_requests = graphene.List(AbsentRequestType, year=graphene.Int(), month=graphene.Int())
    current_other_classes = graphene

    @staticmethod
    def resolve_students_by_code(_, info, code):
        gym = info.context.user.gym
        print(gym)
        parents = Parent.objects.filter(user__phone__endswith=code)
        students = []
        for parent in parents:
            for student in parent.students.filter(is_deleted=False):
                if gym.id == student.class_master.gym_id:
                    print(student)
                    students.append(student)
        return students

    @staticmethod
    def resolve_gym_absent_requests(_, info, year, month):
        gym = info.context.user.gym
        students = Student.objects.filter(class_master__gym=gym,is_deleted=False)
        return AbsentRequest.objects.filter(student__in=students, date_absent__year=year, date_absent__month=month) \
            .distinct()

    @staticmethod
    def resolve_my_children(_, info, ):
        parent = info.context.user.parent
        return Student.objects.filter(parent=parent,is_deleted=False)

    @staticmethod
    def resolve_relationships(_, __, ):
        return Relationship.objects.all()

    @staticmethod
    def resolve_parent(_, __, phone):
        try:
            return Parent.objects.get(user__phone=phone)
        except ObjectDoesNotExist:
            return

    @staticmethod
    def resolve_my_schools(_, info):
        gym = info.context.user.gym
        students = Student.objects.filter(class_master__gym=gym, is_deleted=False)
        schools = []
        for student in students:
            if student.school not in schools:
                schools.append(student.school)
        return schools

    @staticmethod
    def resolve_all_students(_, info):
        gym = info.context.user.gym
        return Student.objects.filter(class_master__gym=gym, is_deleted=False)

    @staticmethod
    def resolve_students(_, info, class_master_id=None, level_id=None, school_id=None, ):
        gym = info.context.user.gym
        if class_master_id:
            class_masters = ClassMaster.objects.filter(pk=class_master_id, gym=gym)
        else:
            class_masters = gym.class_masters.all()
        if level_id:
            levels = Level.objects.filter(pk=level_id, gym=gym)
        else:
            levels = gym.levels.all()
        if school_id:
            schools = School.objects.filter(pk=school_id)
        else:
            schools = School.objects.all()
        return Student.objects.filter(class_master__in=class_masters, level__in=levels,
                                      school__in=schools)

    @staticmethod
    def resolve_student(_, __, id):
        return Student.objects.get(pk=id)

    @staticmethod
    def resolve_audition_master(_, info, state):
        gym = info.context.user.gym
        return AuditionMaster.objects.filter(gym=gym, state=state)

    @staticmethod
    def resolve_audition_detail(_, __, audition_master_id):
        audition_master = AuditionMaster.objects.get(pk=audition_master_id)
        return AuditionDetail.objects.filter(audition_master=audition_master)

    @staticmethod
    def resolve_student_schedule_for_parent(_, info, date):
        parent = info.context.user.parent.get()
        students = parent.students.all()
        attendance_str = ""
        attendance_out_str = ""
        absent_str = ""
        other_class_str = ""
        other_class_out_str = ""
        attendance_masters = AttendanceMaster.objects.filter(date=date)
        for attendance_master in attendance_masters:
            attendance_details = attendance_master.attendance_details.filter(student__in=students)
            for attendance_detail in attendance_details:
                if attendance_detail.type == "등원":
                    attendance_str += "{} {} {}시 {}분에 등원하였습니다.".format(
                        attendance_detail.attendance_master.class_master.name,
                        attendance_detail.student.name,
                        attendance_detail.date_attended.hour,
                        attendance_detail.date_attended.minute)

                elif attendance_detail.type == "하원":
                    attendance_str += "{} {} {}시 {}분에 등원하였습니다.".format(
                        attendance_detail.attendance_master.class_master.name,
                        attendance_detail.student.name,
                        attendance_detail.date_attended.hour,
                        attendance_detail.date_attended.minute)
                    attendance_out_str += "{} {} {}시 {}분에 하원하였습니다.".format(
                        attendance_detail.attendance_master.class_master.name,
                        attendance_detail.student.name,
                        attendance_detail.date_attended.hour,
                        attendance_detail.date_attended.minute + 10)
                elif attendance_detail.type == "타수업등원":
                    other_class_str += "{} {} {}에 타수업등원하였습니다.".format(
                        attendance_detail.attendance_master.class_master.name,
                        attendance_detail.student.name,
                        attendance_detail.date_attended)
                    other_class_out_str += "{} {} {}시 {}분에 하원하였습니다.".format(
                        attendance_detail.attendance_master.class_master.name,
                        attendance_detail.student.name,
                        attendance_detail.attendance_master.class_detail.hour_end,
                        attendance_detail.attendance_master.class_detail.min_end + 10)
                else:
                    absent_str += "{} {} 결석하였습니다.".format(attendance_detail.attendance_master.class_master,
                                                          attendance_detail.student.name)

        audition_detail_str = ""
        audition_details = AuditionDetail.objects.filter(student__in=students, audition_master__date_audition=date)
        print(audition_details)
        for audition_detail in audition_details:
            print('in')
            audition_detail_str += "{} {} 승급예정일입니다.".format(audition_detail.student.class_master.name,
                                                            audition_detail.student.name)
        print(0)
        schedule_dic = {
            'attendance_str': attendance_str,
            'attendance_out_str': attendance_out_str,
            'other_class_out_str': other_class_out_str,
            'other_class_str': other_class_str,
            'absent_str': absent_str,
            'audition_detail_str': audition_detail_str
        }
        return schedule_dic

    @staticmethod
    def resolve_student_statistics(_, info, **kwargs):
        gym = info.context.user.gym
        print(gym)
        gym_created = gym.date_created
        gym_created_year = int(gym_created.strftime('%Y'))
        gym_created_month = int(gym_created.strftime('%m'))
        gym_created_day = int(gym_created.strftime('%d'))
        class_master_name = kwargs.get('class_master_name')
        year = kwargs.get('year')
        if class_master_name:
            class_masters = ClassMaster.objects.filter(name=class_master_name,
                                                       gym=gym)
        else:
            class_masters = gym.class_masters.all()
        if year == datetime.today().year:
            month = datetime.today().month
        else:
            month = 12
        statistic_list = []
        for i in range(month):
            if date(gym_created_year, gym_created_month, 1) <= date(year, i + 1, 1):
                total_student = 0
                new_student = 0
                out_student = 0
                for class_master in class_masters:
                    if i + 1 == 12:
                        students = class_master.students.all()
                        for student in students:
                            if student.date_entered < datetime(year=year,
                                                               month=((i + 1) % 12) + 1,
                                                               day=31).date():
                                if student.date_exit is None or student.date_exit > datetime(year=year,
                                                                                             month=((i + 1) % 12 + 1),
                                                                                             day=31).date():
                                    total_student += 1
                    else:
                        students = class_master.students.all()
                        for student in students:
                            if student.date_entered < datetime(year=year,
                                                             month=((i+1)%12)+1,
                                                             day=1).date():
                                if student.date_exit is None or student.date_exit > datetime(year=year,
                                                                                             month=((i+1)%12+1),
                                                                                             day=1).date():
                                    total_student += 1
                    new_student += class_master.students.filter(date_entered__year=year,
                                                                date_entered__month=i + 1).count()
                    out_student += class_master.students.filter(date_exit__year=year,
                                                                date_exit__month=i + 1).count()

                statistic_dic = {
                    'month': i + 1,
                    'total_student': total_student,
                    'new_student': new_student,
                    'out_student': out_student
                }
                statistic_list.append(statistic_dic)

            else:
                pass
        return statistic_list


class Mutation(graphene.ObjectType):
    create_student = CreateStudent.Field()
    update_students = UpdateStudents.Field()
    delete_student = DeleteStudent.Field()
    create_audition = CreateAudition.Field()
    audition_detail_pass = AuditionDetailPass.Field()
    audition_master_pass = AuditionMasterPass.Field()
    add_audition_detail = AddAuditionDetail.Field()
    delete_audition_detail = DeleteAuditionDetail.Field()
    delete_audition_master = DeleteAuditionMaster.Field()
    student_attendance = StudentAttendance.Field()
    other_class_attendance = OtherClassAttendance.Field()
    attendance_for_student = AttendanceForStudent.Field()
    attendance_for_all_classes = AttendanceForAllClasses()
    update_parent = UpdateParent.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
