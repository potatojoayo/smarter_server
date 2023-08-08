from django.db.models import Value, Q
from django.db.models.functions import Replace
from graphene_django.filter import DjangoFilterConnectionField


class ChargeOrderField(DjangoFilterConnectionField):

    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs

        keyword = args.get('keyword', None)
        if keyword:
            keyword = keyword.replace(' ', '')
            qs = qs.annotate(gym_name=Replace('user__gym__name', Value(' '), Value(''))).filter(
                Q(user__identification__icontains=keyword) | Q(user__name__icontains=keyword)
                | Q(gym_name__icontains=keyword) | Q(
                    user__phone__icontains=keyword))

        qs = qs.exclude(state='충전요청').order_by('-date_created')


        return qs
