user_creation_mutation = """
                    mutation TestMutation($user: UserInput!) {
                        create_user(input: $user) {
                            ... on UserType {
                              email
                              name_first
                              name_last
                              user_handle
                            }
                            ... on OperationInfo {
                                __typename
                                messages {
                                    field
                                    kind
                                    message
                                }
                            }
                        }
                    }
                """

picture_creation_mutation = """
                    mutation TestMutation($picture: PictureInput!) {
                        create_picture(input: $picture) {
                            ... on PictureType {
                              user {
                                email
                              }
                              picture_path
                              likes {
                                email
                              }
                            }
                            ... on OperationInfo {
                                __typename
                                messages {
                                    field
                                    kind
                                    message
                                }
                            }
                        }
                    }
                """
