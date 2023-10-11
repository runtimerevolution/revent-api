picture_creation_mutation = """
                    mutation TestMutation($picture: PictureInput!, $upload: Upload!) {
                        create_picture(input: $picture, picture: $upload) {
                            ... on PictureType {
                              id
                              user {
                                id
                              }
                              file
                              likes {
                                id
                              }
                            }
                        }
                    }
                """
