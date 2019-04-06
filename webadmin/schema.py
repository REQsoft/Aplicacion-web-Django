import graphene
import graphql_jwt
import services.schema, config.schema, connections.schema




class Query(services.schema.Query, 
            graphene.ObjectType):
    '''This class will inherit from multiple Queries
    as we begin to add more apps to our project'''

    pass

class Mutations(graphene.ObjectType):
    '''This class will generate a new token to 
    authenticate and clasificate all the users that 
    send a request to our API'''

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)
