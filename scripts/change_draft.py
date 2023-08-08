from django.db import transaction

from authentication.models import User
from order.models import OrderDetail
from product.models import Draft, NewDraft, DraftSize


@transaction.atomic()
def run():
    users = User.objects.filter(groups__name='체육관')
    for user in users:
        print('user name')
        print(user.name)
        inserted_draft_images = []
        drafts = user.drafts.all()
        for draft in drafts:
            if draft.draft_image is not None:
                image = draft.draft_image.image
            else:
                image = draft.image
            print(image)
            print(draft)
            if image in inserted_draft_images:
                new_draft = NewDraft.objects.get(user=user, image=image)

            else:
                inserted_draft_images.append(image)
                new_draft = NewDraft.objects.create(
                    draft_request=draft.draft_request,
                    image=image,
                    user=user,
                    sub_category=draft.product_master.sub_category,
                    price_work=draft.price_work,
                    price_work_labor=draft.price_work_labor,
                    memo=draft.memo,
                    font=draft.font,
                    thread_color=draft.thread_color,
                    is_deleted=draft.is_deleted)
                for index in range(6):
                    DraftSize.objects.create(new_draft=new_draft, name='사이즈 {}'.format(index + 1))

            order_details = draft.orders.all()
            for order_detail in order_details:
                order_detail.new_draft = new_draft

                order_detail.save()
            work_details = draft.works.all()
            for work_detail in work_details:
                work_detail.new_draft = new_draft
                work_detail.save()
