import graphene

from gym_class.models import Level
from gym_class.types.level_input_type import LevelInputType


class CreateOrUpdateLevel(graphene.Mutation):
    class Arguments:
        level_object = LevelInputType()
        delete = graphene.Boolean()

    success = graphene.Boolean(default_value=False)
    student_exists = graphene.Boolean(default_value=False)
    deleted = graphene.Boolean(default_value=False)
    is_duplicated = graphene.Boolean(default_value=False)
    @classmethod
    def mutate(cls, _, info, level_object, delete=False):
        gym = info.context.user.gym
        print(level_object)
        if level_object.id:
            level = Level.objects.get(pk=level_object.id)
            if Level.objects.filter(gym=gym, name=level_object.name) and level.name != level_object.name:
                return CreateOrUpdateLevel(success=False, is_duplicated=True)
            if delete:
                student_exists = level.students.exists()
                if student_exists:
                    return CreateOrUpdateLevel(success=False, student_exists=True)
                level.delete()
                return CreateOrUpdateLevel(success=True, deleted=True)
            level.name = level_object.name
            level.belt = level_object.belt
            level.belt_color = level_object.belt_color
            level.belt_brand = level_object.belt_brand
            level.save()
        else:
            last = Level.objects.filter(gym=gym).order_by('-order')
            order = 0
            if last.exists():
                order = last.first().order + 1
            if Level.objects.filter(gym=gym, name=level_object.name):
                return CreateOrUpdateLevel(success=False, is_duplicated=True)
            Level.objects.create(gym=gym,
                                 name=level_object.name,
                                 belt=level_object.belt,
                                 belt_color=level_object.belt_color,
                                 belt_brand=level_object.belt_brand,
                                 order=order)


        return CreateOrUpdateLevel(success=True)
