from graphene_django.filter import DjangoFilterConnectionField


class MyChildrenAuditionField(DjangoFilterConnectionField):

    @classmethod
    def resolve_queryset(
            cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs

        parent = info.context.user.parent
        students = parent.students.all()
        year = args.get('year', None)
        month = args.get('month', None)
        qs = qs.filter(audition_details__student__in=students,
                       date_audition__year=year,
                       date_audition__month=month
                       ).distinct()

        return qs
