import graphene
from dateutil import parser
from django.db import transaction

from gym_class.models import Level
from gym_student.methods.audition_date_alarm import audition_date_alarm_main
from gym_student.models import AuditionMaster, Student, AuditionDetail
from gym_student.types.audition_master.audition_master_input_type import AuditionMasterInputType


class CreateAudition(graphene.Mutation):
    class Arguments:
        audition_master_objects = graphene.List(AuditionMasterInputType)
        date_audition = graphene.String()
        date_alarm = graphene.String()
    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info, audition_master_objects, date_audition, date_alarm):
        user = info.context.user
        gym = user.gym
        date_audition = parser.parse(date_audition)
        date_alarm = parser.parse(date_alarm)
        audition_master_ids = []
        for audition_master_object in audition_master_objects:
            current_level = Level.objects.get(name=audition_master_object.current_level, gym=gym)
            next_level = Level.objects.get(name=audition_master_object.next_level, gym=gym)
            audition_master = AuditionMaster.objects.create(current_level=current_level,
                                                            next_level=next_level,
                                                            date_audition=date_audition,
                                                            gym=gym)
            students = Student.objects.filter(class_master__gym=gym,
                                              level=current_level)
            for student in students:
                AuditionDetail.objects.create(student=student,
                                              audition_master=audition_master)

            audition_master_ids.append(audition_master.id)
        gym_id = gym.id
        audition_date_alarm_main(date_alarm, audition_master_ids, gym_id)
        return CreateAudition(success=True)