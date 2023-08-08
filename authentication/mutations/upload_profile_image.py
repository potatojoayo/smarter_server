import graphene
from graphene_file_upload.scalars import Upload

from authentication.models import User
from authentication.types import UserType
from authentication.types.user_input_type import UserInputType


class UploadProfileImage(graphene.Mutation):
    class Arguments:
        profile_image = Upload()

    success = graphene.Boolean(default_value=False)

    @classmethod
    def mutate(cls, _, info, profile_image):
        try:
            user = info.context.user
            user.profile_image = profile_image
            user.save()
            return UploadProfileImage(success=True)
        except Exception as e:
            print(e)
            return UploadProfileImage()
