from graphene_django.filter import DjangoFilterConnectionField


class AttendanceField(DjangoFilterConnectionField):

    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        print(qs)
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs

        gym = info.context.user.gym
        qs = qs.filter(gym=gym).order_by('-date')
        print(qs)
        return qs
