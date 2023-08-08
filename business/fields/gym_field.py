from django.db.models import Q, Count
from graphene_django.filter import DjangoFilterConnectionField



class GymField(DjangoFilterConnectionField):

    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs.distinct().order_by('-date_created')
        user = info.context.user
        try:
            if user.agency:
                qs = qs.filter(user__gym__agency=user.agency)
        except:
            pass

        keyword = args.get('keyword', None)
        if keyword:
            query = Q(name__icontains=keyword)
            query.add(Q(user__identification__icontains=keyword), Q.OR)
            query.add(Q(user__name__icontains=keyword), Q.OR)
            print(query)
            qs = qs.filter(query)

        draft_exists = args.get('draft_exists', None)

        if draft_exists is not None:
            if draft_exists:
                qs = qs.annotate(num_draft=Count('user__drafts')).filter(num_draft__gt=0)
            else:
                qs = qs.annotate(num_draft=Count('user__drafts')).filter(num_draft=0)

        return qs
