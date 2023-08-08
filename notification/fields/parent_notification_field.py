from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Q

from authentication.models import User


class ParentNotificationField(DjangoFilterConnectionField):

    @classmethod
    def resolve_queryset(
            cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs

        user = User.objects.get(pk=45)
        students = user.parent.students.all()
        # students = info.context.user.parent.students.all()
        qs = qs.filter(parent=user.parent)
        print(qs)

        year = args.get('year', None)
        if year:
            month = args.get('month', None)
            qs = qs.filter(event_date__year=year, event_date__month=month).order_by('event_date')

        return qs
