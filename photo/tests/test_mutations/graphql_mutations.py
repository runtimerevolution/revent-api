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

user_delete_mutation = """
                    mutation TestMutation($user: UserFilter!) {
                        delete_user(input: $user) {
                            ... on UserType {
                              id
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
                    mutation TestMutation($input: PictureInput!) {
                        create_picture(input: $input) {
                            ... on CreatePictureMutationResponse {
                              success
                              results {
                                id
                                user {
                                  id
                                }
                                file
                                likes {
                                  id
                                }
                              }
                              errors
                            }
                        }
                    }
                """

picture_like_mutation = """
                    mutation TestMutation($user: String!, $picture: Int!) {
                        like_picture(user: $user, picture: $picture) {
                            ... on AddLikeMutationResponse {
                              success
                              results {
                                id
                                user {
                                  id
                                }
                                file
                                likes {
                                  id
                                }
                              }
                              errors
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

picture_delete_mutation = """
                    mutation TestMutation($picture: PictureFilter!) {
                        delete_picture(input: $picture) {
                            ... on PictureType {
                              id
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
                        create_picture_comment(input: $pictureComment) {
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
                        update_picture_comment(input: $pictureComment) {
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

picture_comment_delete_mutation = """
                    mutation TestMutation($picture_comment: PictureCommentFilter!) {
                        delete_picture_comment(input: $picture_comment) {
                            ... on PictureCommentType {
                              id
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
                            ... on CollectionAddPictureMutationResponse {
                              success
                              results {
                                user {
                                  email
                                }
                                name
                                pictures {
                                  id
                                }
                              }
                              errors
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

collection_delete_mutation = """
                    mutation TestMutation($collection: CollectionFilter!) {
                        delete_collection(input: $collection) {
                            ... on CollectionType {
                              id
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
                            ... on CloseContestMutationResponse {
                              success
                              results {
                                id
                                voting_phase_end
                              }
                              errors
                            }
                        }
                    }
                """

contest_delete_mutation = """
                    mutation TestMutation($contest: ContestFilter!) {
                        delete_contest(input: $contest) {
                            ... on ContestType {
                              id
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
                        create_contest_submission(input: $contestSubmission) {
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
                        update_contest_submission(input: $contestSubmission) {
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
                            ... on AddVoteMutationResponse {
                              success
                              results {
                                id
                                votes {
                                  email
                                }
                              }
                              errors
                            }
                        }
                    }
                """

contest_submission_delete_mutation = """
                    mutation TestMutation($contest_submission: ContestSubmissionFilter!) {
                        delete_contest_submission(input: $contest_submission) {
                            ... on ContestSubmissionType {
                              id
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
