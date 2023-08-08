from graphene_django.filter import DjangoFilterConnectionField

from gym_student.models import Parent


class IsApprovedClassPaymentMasterField(DjangoFilterConnectionField):

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
        qs = qs.filter(student__parent=parent, is_approved=True)

        return qs
