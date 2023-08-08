import graphene

from inventory.models import Supplier
from inventory.types.supplier_input_type import SupplierInputType
from inventory.types.supplier_type import SupplierType


class UpdateSupplier(graphene.Mutation):

    class Arguments:
        supplier = SupplierInputType()

    supplier = graphene.Field(SupplierType)

    @classmethod
    def mutate(cls, _, __, supplier):

        # 새로운 거래처 생성
        if not supplier.id:
            new_supplier = Supplier.objects.create(**supplier)
            return UpdateSupplier(supplier=new_supplier)

        # 기존 거래처 업데이트
        Supplier.objects.filter(pk=supplier.id).update(name=supplier.name,
                                                       address=supplier.address,
                                                       manager=supplier.manager,
                                                       phone=supplier.phone,
                                                       fax=supplier.fax,
                                                       email=supplier.email,
                                                       business_registration_number=
                                                       supplier.business_registration_number,
                                                       )

        if supplier.business_registration_certificate is not None:
            old_supplier = Supplier.objects.get(pk=supplier.id)
            old_supplier.business_registration_certificate  = supplier.business_registration_certificate
            old_supplier.save()

        return UpdateSupplier(supplier=Supplier.objects.get(pk=supplier.id))







