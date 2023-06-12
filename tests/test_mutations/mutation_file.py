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

picture_comment_creation_mutation = """
                    mutation TestMutation($pictureComment: PictureCommentInput!) {
                        create_pictureComment(input: $pictureComment) {
                            ... on PictureCommentType {
                              user {
                                email
                              }
                              picture {
                                picture_path
                              }
                              text
                              created_at
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

collection_creation_mutation = """
                    mutation TestMutation($collection: CollectionInput!) {
                        create_collection(input: $collection) {
                            ... on CollectionType {
                              user {
                                email
                              }
                              name
                              pictures {
                                picture_path
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

contest_creation_mutation = """
                    mutation TestMutation($contest: ContestInput!) {
                        create_contest(input: $contest) {
                            ... on ContestType {
                                id
                                title
                                description
                                created_by {
                                    email
                                }
                                cover_picture {
                                    picture_path
                                }
                                prize
                                automated_dates
                                upload_phase_start
                                upload_phase_end
                                voting_phase_end
                                active
                                winners {
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

contest_submission_creation_mutation = """
                    mutation TestMutation($contestSubmission: ContestSubmissionInput!) {
                        create_contestSubmission(input: $contestSubmission) {
                            ... on ContestSubmissionType {
                                contest {
                                    id
                                }
                                picture {
                                    picture_path
                                    user {
                                        email
                                    }
                                }
                                submission_date
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
