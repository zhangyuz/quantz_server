import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from quantz_repo import IndexDailyItem as IndexDailyItemModel


class IndexDailyItem(MongoengineObjectType):

    class Meta:
        model = IndexDailyItemModel
        interfaces = (Node,)


class Query(graphene.ObjectType):
    index_daily = MongoengineConnectionField(IndexDailyItem)


schema = graphene.Schema(query=Query, types=[IndexDailyItem])
