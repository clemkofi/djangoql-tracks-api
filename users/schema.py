import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

# using the in-built django user model we make a usertype for graphene
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        # the only fields property helps to limit the values to be displayed 
        # use field names in db
        # fields = ('id', 'email', 'username', 'password', 'date_joined')


# class to handle user creation mutation
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)


    # function to perform mutation logic
    def mutate(self, info, **kwags):
        if kwags.get('username') == "" or kwags.get('email') == "" or kwags.get('password') == "":
            raise GraphQLError('Incorrect Argument for User Details')
        user = get_user_model()(
            username = kwags.get('username'),
            email = kwags.get('email')
        )

        user.set_password(kwags.get('password'))
        user.save()
        return CreateUser(user=user)

# root query for users
class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    me = graphene.Field(UserType)

    # resolver to get user by id
    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

    # resolver for me
    def resolve_me(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Not logged In')

        return get_user_model().objects.get(username=user)

# root mutation for users
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()