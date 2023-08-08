from datetime import datetime
from dateutil.relativedelta import relativedelta
from graphene_django.filter import DjangoFilterConnectionField


class RecentOrderedProductsField(DjangoFilterConnectionField):

    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super(DjangoFilterConnectionField, cls).resolve_queryset(
            connection, iterable, info, args
        )
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs

        user = info.context.user
        orders = user.orders.filter(date_created__gte=datetime.now() - relativedelta(months=1)).order_by('-date_created')
        products = []
        for order in orders:
            for detail in order.details.all():
                if detail.product_master not in products:
                    products.append(detail.product_master.id)
        qs = qs.filter(pk__in=products)

        return qs
