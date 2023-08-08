from datetime import datetime

import pytz
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Q



class ChildrenNotificationField(DjangoFilterConnectionField):

    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs

        students = info.context.user.parent.students.all()
        gyms = []
        class_masters = []
        for student in students:
            gyms.append(student.class_master.gym)
            class_masters.append(student.class_master)
        qs = qs.filter(Q(gym__in=gyms, type='전체') | Q(class_master__in=class_masters, type='클래스')).order_by('-date_created')

        year = args.get('year', None)
        if year:
            month = args.get('month', None)
            qs = qs.filter(event_date__year=year, event_date__month=month).order_by('send_datetime')
        timezone_seoul = pytz.timezone('Asia/Seoul')
        now_time = datetime.now()
        now = timezone_seoul.localize(now_time)
        qs_id_list = []
        for q in qs:
            if q.send_datetime <= now:
                qs_id_list.append(q.id)
        qs = qs.filter(pk__in=qs_id_list)
        return qs
