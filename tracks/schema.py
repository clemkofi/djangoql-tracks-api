import graphene
from graphql import GraphQLError
from .models import Track, Like
from graphene_django import DjangoObjectType
from users.schema import UserType
from django.db.models import Q


# class as helper for schema for Tracks
class TrackType(DjangoObjectType):
    # import track structure and fields from Track Model
    class Meta:
        model = Track
        # fields = ('title', 'description','url',)

# class as helper for schema
class LikeType(DjangoObjectType):
    class Meta:
        model = Like


# class for the track creation
class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    # arguments for the mutation
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    # function that is run when the mutation is called
    def mutate(self, info, **kwargs):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("Not logged In!")

        track = Track(
            title = kwargs.get('title'), 
            description = kwargs.get('description'),
            url = kwargs.get('url'),
            postedBy = user,
            )

        track.save()
        return CreateTrack(track=track)


# class for track update mutation
class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    # function to run for the update mutation
    def mutate(self, info, **kwargs):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("Not logged In!")

        track = Track.objects.get(id=kwargs.get('track_id'))

        # check for whether current logged in user posted the track
        if track.postedBy != user:
            raise GraphQLError("Track posted by another user.... Update not successful!")

        track.title = kwargs.get('title')
        track.description = kwargs.get('description')
        track.url = kwargs.get('url')

        track.save()
        return UpdateTrack(track=track)


# class for track deletion
class DeleteTrack(graphene.Mutation):
    # only the id of track is needed for the deletion
    track_id = graphene.Int()

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user
        track = Track.objects.get(id=track_id)

        # check for whether current logged in user posted the track
        if track.postedBy != user:
            raise GraphQLError("Track posted by another user.... Delete not successful!")

        track.delete()
        return DeleteTrack(track_id=track_id)


# class for mutation for creating likes for Tracks
class CreateLike(graphene.Mutation):
    track = graphene.Field(TrackType)
    user = graphene.Field(UserType)

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("Not logged In!")

        track = Track.objects.get(id=track_id) 

        # check if track exists
        if not track:
            raise GraphQLError("Track does not exist")

        # create the link between the users and tracks for the likes
        Like.objects.create(
            user=user,
            track=track
        )

        return CreateLike(user=user, track=track)


# class for the track querys
class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType, search=graphene.String())
    likes = graphene.List(LikeType)

    # resolver to help read or get data from Track table
    def resolve_tracks(self, info, search=None):
        if search:
            # filter to contain multiply queries in order to perform a needle in the haystack search
            filter = (
                Q(title__icontains = search) | 
                Q(description__icontains = search) |
                Q(url__icontains = search) | 
                Q(postedBy__username__icontains=search)
            )

            return Track.objects.filter(filter)
        return Track.objects.all()

    # resolver for the likes 
    def resolve_likes(self, info):
        return Like.objects.all()

# root class for all track mutation
class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
    create_like = CreateLike.Field()