from graphene_django.filter import DjangoFilterConnectionField


class UserFilteredDjangoFilterConnectionField(DjangoFilterConnectionField):

    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs

        # order = args.get('orderBy', None)
        # if order:
        #     if type(order) is str:
        #         snake_order = to_snake_case(order)
        #     else:
        #         snake_order = [to_snake_case(o) for o in order]
        #     print(snake_order)
        #     qs = qs.order_by(snake_order)

        user = info.context.user
        qs = qs.filter(user=user).order_by('-date_created')

        return qs
