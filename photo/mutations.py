
@strawberry.mutation
def create_picture(self, input: PictureInput) -> CreatePictureMutationResponse:
    try:
        image_file = save_image_file(input.file)
        picture_object = Picture.objects.create(
            user_id=input.user,
            file=image_file,
            description=input.get('description', None)
        )
        return CreatePictureMutationResponse(
            success=True, results=picture_object, errors=""
        )
    except ValidationError as e:
        return CreatePictureMutationResponse(
            success=False, results={}, errors=e.message
        )
    except DatabaseError:
        return CreatePictureMutationResponse(
            success=False, results={}, errors=CREATE_PICTURE_ERROR
        )