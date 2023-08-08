from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Q, Value
from django.db.models.functions import Replace

from order.models import Work


class WorkField(DjangoFilterConnectionField):

    @classmethod
    def resolve_queryset(
            cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs.distinct().order_by('-date_created')

        keyword = args.get('keyword', None)
        ids = args.get('ids')
        if keyword:
            keyword = keyword.replace(' ', '')
            qs = qs.annotate(gym_name=Replace('order_master__user__gym__name', Value(' '), Value(''))).filter(
                Q(order_master__user__identification__icontains=keyword) | Q(order_master__user__name__icontains=keyword)
                | Q(order_master__user__phone__icontains=keyword) | Q(gym_name__icontains=keyword)
                )
        if ids:
            qs = qs.filter(id__in=ids)
        qs = qs.order_by('-date_created')
        return qs
