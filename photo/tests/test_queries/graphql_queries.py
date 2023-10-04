# File with the queries used by the tests

collections_query_all = """
                            query TestQuery {
                                collections {
                                    id
                                    name
                                    user {
                                        id
                                    }
                                    pictures {
                                        id
                                    }
                                }
                            }
                        """


collections_query_filter = """
                    query TestQuery($filters: CollectionFilter!) {
                        collections(filters: $filters) {
                            id
                            name
                            user {
                                id
                            }
                            pictures {
                                id
                            }
                        }
                    }
                """


contest_query_all = """
                    query TestQuery {
                        contests {
                            id
                            title
                            description
                            created_by {
                                id
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
                                id
                            }
                            status
                        }
                    }
                """


contest_query_filters = """
                    query TestQuery($filters: ContestFilter!) {
                        contests(filters: $filters) {
                            id
                            title
                            description
                            created_by {
                                id
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
                                id
                            }
                            status
                        }
                    }
                """

contest_query_search = """
                    query TestQuery($search: String!) {
                        contest_search(search: $search) {
                            id
                            title
                            description
                            prize
                        }
                    }
                """

contest_submission_query_all = """
                    query TestQuery {
                        contest_submissions {
                            id
                            contest {
                                id
                            }
                            picture {
                                id
                                user {
                                    id
                                }
                            }
                            submission_date
                            votes {
                                email
                            }
                        }
                    }
                """


contest_submission_query_filters = """
                    query TestQuery($filters: ContestSubmissionFilter!) {
                        contest_submissions(filters: $filters) {
                            id
                            contest {
                                id
                            }
                            picture {
                                id
                                user {
                                    id
                                }
                            }
                            submission_date
                            votes {
                                email
                            }
                        }
                    }
                """

picture_query_all = """
                    query TestQuery {
                        pictures {
                            id
                            user {
                                id
                            }
                            file
                            likes {
                                email
                            }
                        }
                    }
                """

picture_query_filters = """
                    query TestQuery($filters: PictureFilter!) {
                        pictures(filters: $filters) {
                            id
                            user {
                                id
                            }
                            file
                            likes {
                                email
                            }
                        }
                    }
                """

picture_comment_query_all = """
                    query TestQuery {
                        picture_comments {
                            id
                            user {
                                email
                            }
                            picture {
                                id
                            }
                            text
                            created_at
                        }
                    }
                """

picture_comment_query_filters = """
                    query TestQuery($filters: PictureCommentFilter!) {
                        picture_comments(filters: $filters) {
                            id
                            user {
                                id
                            }
                            picture {
                                id
                            }
                            text
                            created_at
                        }
                    }
                """


user_query_one = """
                    query TestQuery($user: UUID!) {
                        users(user: $user) {
                            email
                        }
                    }
                """
