import graphene

import class_payment.schema
import cs.schema
import gym_student.schema
import gym_class.schema
import notification.schema
import product.schema
import authentication.schema
import order.schema
import common.schema
import business.schema
import inventory.schema
import authentication.schema
import smarter_money.schema
import payment.schema
import calculate.schema
import gym_class.schema
import statistic.schema


class Query(product.schema.Query,
            authentication.schema.Query,
            order.schema.Query,
            common.schema.Query,
            business.schema.Query,
            inventory.schema.Query,
            smarter_money.schema.Query,
            calculate.schema.Query,
            gym_class.schema.Query,
            gym_student.schema.Query,
            statistic.schema.Query,
            class_payment.schema.Query,
            notification.schema.Query,
            cs.schema.Query,
            ):
    pass


class Mutation(product.schema.Mutation,
               authentication.schema.Mutation,
               inventory.schema.Mutation,
               order.schema.Mutation,
               business.schema.Mutation,
               common.schema.Mutation,
               smarter_money.schema.Mutation,
               payment.schema.Mutation,
               calculate.schema.Mutation,
               gym_student.schema.Mutation,
               gym_class.schema.Mutation,
               class_payment.schema.Mutation,
               notification.schema.Mutation,
               cs.schema.Mutation,
               ):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

