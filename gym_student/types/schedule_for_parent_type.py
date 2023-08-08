import graphene


class ScheduleForParentType(graphene.ObjectType):
    attendance_str = graphene.String()
    attendance_out_str = graphene.String()
    absent_str = graphene.String()
    other_class_str = graphene.String()
    other_class_out_str = graphene.String()
    audition_detail_str = graphene.String()
