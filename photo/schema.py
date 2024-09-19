
import graphene
from graphene_django.types import DjangoObjectType
from .models import Picture

class PictureType(DjangoObjectType):
    class Meta:
        model = Picture

class PictureInput(graphene.InputObjectType):
    file = graphene.String()
    user = graphene.ID()
    description = graphene.String()

class PictureInputPartial(graphene.InputObjectType):
    id = graphene.ID(required=True)

class PictureQuery(graphene.ObjectType):
    pictures = graphene.List(PictureType)

class PictureMutation(graphene.ObjectType):
    create_picture = CreatePicture.Field()
    update_picture = UpdatePicture.Field()
    delete_picture = DeletePicture.Field()
    like_picture = LikePicture.Field()
    unlike_picture = UnlikePicture.Field()