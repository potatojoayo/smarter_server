import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from authentication.mutations.create_or_update_agency import CreateOrUpdateAgency
from authentication.mutations.create_or_update_gym import CreateOrUpdateGym
from authentication.mutations.create_or_update_subcontractor import CreateOrUpdateSubcontractor
from authentication.mutations.update_gym import UpdateGym
from order.fields.distinct_field import DistinctField
from order.models import OrderDetail, Work
from .fields.gym_field import GymField
from .models import Subcontractor
from .mutations.UpdateGymMemo import UpdateGymMemo
from .types.agency.agency_node import AgencyNode
from .types.gym.gym_node import GymNode
from .types.subcontractor.subcontractor_node import SubcontractorNode
from .types.subcontractor.subcontractor_type import SubcontractorType


class Query(graphene.ObjectType):
    gyms = GymField(GymNode, keyword=graphene.String(), draft_exists=graphene.Boolean())
    gym = relay.Node.Field(GymNode)
    agencies = DjangoFilterConnectionField(AgencyNode)
    agency = relay.Node.Field(AgencyNode)
    subcontractors = graphene.List(SubcontractorType, is_out_working=graphene.Boolean(), is_pre_working=graphene.Boolean())
    subcontractor = relay.Node.Field(SubcontractorNode)
    subcontractor_nodes = DjangoFilterConnectionField(SubcontractorNode)

    @staticmethod
    @login_required
    def resolve_subcontractors(_, info, is_out_working=None, is_pre_working=None):
        user = info.context.user
        try:
            subcontractor = user.subcontractor
            return [subcontractor]
        except:
            subcontractors = Subcontractor.objects.filter()
            if is_out_working is not None:
                subcontractors = subcontractors.filter(is_out_working=is_out_working)
            if is_pre_working is not None:
                subcontractors = subcontractors.filter(is_pre_working=is_pre_working)
            return subcontractors

class Mutation(graphene.ObjectType):
    create_or_update_gym = CreateOrUpdateGym.Field()
    create_or_update_agency = CreateOrUpdateAgency.Field()
    create_or_update_subcontractor = CreateOrUpdateSubcontractor.Field()
    update_gym = UpdateGym.Field()
    update_gym_memo = UpdateGymMemo.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

