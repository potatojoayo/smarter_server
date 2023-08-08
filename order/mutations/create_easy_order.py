import graphene
from graphene_file_upload.scalars import Upload
from common.methods.send_notification import send_notification
from order.models import EasyOrder,  EasyOrderFile
from authentication.models import User


class CreateEasyOrder(graphene.Mutation):
    class Arguments:
        contents = graphene.String()
        drafts = graphene.List(Upload)
        files = graphene.List(Upload)
        user_id = graphene.Int()
        is_visit = graphene.Boolean(default_value=False)
        is_order_more = graphene.Boolean(default_value=False)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, info, contents,is_visit, is_order_more, user_id=None, files=None, ):
        if files is None:
            files = []
        if user_id:
            user = User.objects.get(pk=user_id)
        else:
            user = info.context.user
        easy_order = EasyOrder.objects.create(user=user, contents=contents, is_visit=is_visit, is_order_more=is_order_more)
        for file in files:
            EasyOrderFile.objects.create(easy_order=easy_order, file=file)
        #send_notification(user=user, type="간편주문요청", product_names="")
        return CreateEasyOrder(success=True)
