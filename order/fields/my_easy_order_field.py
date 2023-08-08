from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Q


class MyEasyOrderField(DjangoFilterConnectionField):

    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs
        qs = qs.exclude(state='삭제')

        user = info.context.user
        qs = qs.filter(user=user)

        return qs
