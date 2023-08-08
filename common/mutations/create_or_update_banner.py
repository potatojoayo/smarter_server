
import graphene
from django.core.exceptions import ObjectDoesNotExist

from common.models.banner import Banner
from common.types.banner_input_type import BannerInputType


class CreateOrUpdateBanner(graphene.Mutation):
    class Arguments:
        banners = graphene.List(BannerInputType)
        deleting_banner_ids = graphene.List(graphene.Int)
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, banners, deleting_banner_ids=None,):

        for deleting_banner_id in deleting_banner_ids:
            try:
                Banner.objects.get(pk=deleting_banner_id).delete()
            except ObjectDoesNotExist:
                continue

        for banner in banners:
            if banner.id:
                old_banner = Banner.objects.get(pk=banner.id)
                if banner.file:
                    old_banner.image = banner.file
                old_banner.order = banner.order
                old_banner.name = banner.name
                old_banner.save()
            else:
                Banner.objects.create(image=banner.file, order=banner.order, name=banner.name)

        return CreateOrUpdateBanner(success=True)
