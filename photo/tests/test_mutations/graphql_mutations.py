
picture_update_mutation = """
    mutation TestMutation($picture: PictureInputPartial!) {
        update_picture(input: $picture) {
            ... on PictureType {
                id
                user {
                    id
                }
                file
                description
                likes {
                    id
                }
            }
        }
    }

picture_creation_mutation = """
    mutation TestMutation($input: PictureInput!) {
        create_picture(input: $input) {
            ... on PictureType {
                id
                user {
                    id
                }
                file
                description
                likes {
                    id
                }
            }
        }
    }