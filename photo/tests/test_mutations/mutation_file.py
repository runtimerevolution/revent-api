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

user_update_mutation = """
                    mutation TestMutation($user: UserInputPartial!) {
                        update_user(input: $user) {
                            ... on UserType {
                              id
                              email
                              name_first
                              name_last
                              user_handle
                              profile_picture {
                                id
                              }
                              profile_picture_updated_at
                            }
                        }
                    }
                """

picture_creation_mutation = """
                    mutation TestMutation($picture: PictureInput!) {
                        create_picture(input: $picture) {
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

picture_like_mutation = """
                    mutation TestMutation($user: String!, $picture: Int!) {
                        like_picture(user: $user, picture: $picture) {
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

picture_update_mutation = """
                    mutation TestMutation($picture: PictureInputPartial!) {
                        update_picture(input: $picture) {
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

picture_comment_creation_mutation = """
                    mutation TestMutation($pictureComment: PictureCommentInput!) {
                        create_pictureComment(input: $pictureComment) {
                            ... on PictureCommentType {
                              user {
                                id
                              }
                              picture {
                                id
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

picture_comment_update_mutation = """
                    mutation TestMutation($pictureComment: PictureCommentInputPartial!) {
                        update_pictureComment(input: $pictureComment) {
                            ... on PictureCommentType {
                              id
                              user {
                                id
                              }
                              picture {
                                id
                              }
                              text
                            }
                        }
                    }
                """

collection_creation_mutation = """
                    mutation TestMutation($collection: CollectionInput!) {
                        create_collection(input: $collection) {
                            ... on CollectionType {
                              user {
                                id
                              }
                              name
                              pictures {
                                id
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

collection_add_picture_mutation = """
                    mutation TestMutation($collection: Int!, $picture: Int!) {
                        collection_add_picture(collection: $collection, picture: $picture) {
                            ... on CollectionType {
                              user {
                                email
                              }
                              name
                              pictures {
                                id
                              }
                            }
                        }
                    }
                """

collection_update_mutation = """
                    mutation TestMutation($collection: CollectionInputPartial!) {
                        update_collection(input: $collection) {
                            ... on CollectionType {
                              id
                              name
                              pictures {
                                id
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
                                    id
                                }
                                prize
                                automated_dates
                                upload_phase_start
                                upload_phase_end
                                voting_phase_end
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

contest_update_mutation = """
                    mutation TestMutation($contest: ContestInputPartial!) {
                        update_contest(input: $contest) {
                            ... on ContestType {
                              id
                              title
                              description
                              cover_picture {
                                id
                              }
                              prize
                              upload_phase_end
                              voting_phase_end
                            }
                        }
                    }
                """

contest_close_mutation = """
                    mutation TestMutation($contest: Int!) {
                        contest_close(contest: $contest) {
                            ... on ContestType {
                              id
                              voting_phase_end
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
                                    id
                                    file
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

contest_submission_update_mutation = """
                    mutation TestMutation($contestSubmission: ContestSubmissionInputPartial!) {
                        update_contestSubmission(input: $contestSubmission) {
                            ... on ContestSubmissionType {
                              id
                              picture {
                                id
                              }
                              submission_date
                            }
                        }
                    }
                """

contest_submission_vote_mutation = """
                    mutation TestMutation($contestSubmission: Int!, $user: String!) {
                        contest_submission_add_vote(contestSubmission: $contestSubmission, user: $user) {
                            ... on ContestSubmissionType {
                              id
                              votes {
                                email
                              }
                            }
                        }
                    }
                """
