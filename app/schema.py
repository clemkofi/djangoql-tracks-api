import graphene
import tracks.schema as tracksSchema
import users.schema as userSchema
import graphql_jwt

# Root query .... 
# this is the main query for all the other queries that is set up in each app
class Query(
    userSchema.Query,
    tracksSchema.Query, 
    graphene.ObjectType
    ):
    pass

# Root Mutation ....
# main mutation for all mutation
class Mutation(
    userSchema.Mutation,
    tracksSchema.Mutation, 
    graphene.ObjectType
    ):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)