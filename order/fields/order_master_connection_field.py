from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Q, Value
from django.db.models.functions import Replace

from order.models import OrderMaster


class OrderMasterConnectionField(DjangoFilterConnectionField):

    @classmethod
    def resolve_queryset(
            cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}

        user = info.context.user
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs.distinct()
        qs = qs.exclude(details__state='구매요청')
        qs = qs.exclude(details__state='간편주문취소')
        qs = qs.exclude(is_deleted=True)
        qs = qs.exclude(parent_order__isnull=False)
        keyword = args.get('keyword', None)
        state = args.get('state', None)
        if state:
            qs = qs.filter(Q(details__state__in=[state]) | Q(children__details__state__in=[state]))
        if keyword:
            keyword = keyword.replace(' ', '')
            qs = qs.annotate(gym_name=Replace('user__gym__name', Value(' '), Value(''))).filter(
                Q(user__identification__icontains=keyword) | Q(user__name__icontains=keyword)
                | Q(order_number__icontains=keyword) | Q(gym_name__icontains=keyword) | Q(
                    user__phone__icontains=keyword))

        try:
            if user.agency:
                qs = qs.filter(user__gym__agency=user.agency)
        except:
            pass

        return qs
