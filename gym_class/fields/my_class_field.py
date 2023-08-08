from graphene_django.filter import DjangoFilterConnectionField


class MyClassField(DjangoFilterConnectionField):

    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs

        gym = info.context.user.gym
        qs = qs.filter(gym=gym, is_deleted=False).order_by('-date_created')

        return qs
