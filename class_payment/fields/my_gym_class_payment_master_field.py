import datetime

from graphene_django.filter import DjangoFilterConnectionField


class MyGymClassPaymentMasterField(DjangoFilterConnectionField):

    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )

        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        print(filter_kwargs)
        print(qs)
        if 'type' in filter_kwargs:
            if args['type'] == '신규':
                qs = qs.filter(type="신규")
            else:
                qs = qs.exclude(type="신규")
        else:
            print(qs)
            pass

        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs

        gym = info.context.user.gym
        if args['filtering_name'] == "이름순":
            qs = qs.filter(student__class_master__gym=gym).order_by('student__name', '-date_to_pay')
        elif args['filtering_name'] == "날짜순":
            qs = qs.filter(student__class_master__gym=gym).order_by('-date_to_pay')
        elif args['filtering_name'] == "이름역순":
            qs = qs.filter(student__class_master__gym=gym).order_by('-student__name', '-date_to_pay')
        else:
            qs = qs.filter(student__class_master__gym=gym).order_by('-date_to_pay')

        now = datetime.date.today()
        print(qs)
        qs = qs.filter(date_to_pay__gte=now - datetime.timedelta(args['filtering_days']))

        return qs
