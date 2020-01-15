import graphene


import ingredients.schema


class Query(ingredients.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutations(ingredients.schema.MyMutations, graphene.ObjectType):
    pass

schema = graphene.Schema(query = Query, mutation = Mutations)