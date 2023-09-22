# File with the queries used by the tests

collections_query_all = """
                            query TestQuery {
                                collections {
                                    id
                                    name
                                    user {
                                        email
                                    }
                                    pictures {
                                        id
                                    }
                                }
                            }
                        """

collections_query_one = """
                    query TestQuery($id: Int!) {
                        collections(id: $id) {
                            id
                            name
                            user {
                                email
                            }
                            pictures {
                                id
                            }
                        }
                    }
                """

collections_query_user_email = """
                    query TestQuery($user_email: String!, $name: String!) {
                        collections(user_email: $user_email, name: $name) {
                            id
                            name
                            user {
                                email
                            }
                            pictures {
                                id
                            }
                        }
                    }
                """

collections_query_user = """
                    query TestQuery($user_email: String!) {
                        collections(user_email: $user_email) {
                            id
                            name
                            user {
                                email
                            }
                            pictures {
                                id
                            }
                        }
                    }
                """

collections_query_name = """
                    query TestQuery($name: String!) {
                        collections(name: $name) {
                            id
                            name
                            user {
                                email
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
                            status
                        }
                    }
                """

contest_query_one = """
                    query TestQuery($id: Int!) {
                        contests(id: $id) {
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
                            status
                        }
                    }
                """

contest_query_creator = """
                    query TestQuery($user_email: String!) {
                        contests(user_email: $user_email) {
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
                                    email
                                }
                            }
                            submission_date
                            votes {
                                email
                            }
                        }
                    }
                """

contest_submission_query_one = """
                    query TestQuery($id: Int!) {
                        contest_submissions(id: $id) {
                            id
                            contest {
                                id
                            }
                            picture {
                                id
                                user {
                                    email
                                }
                            }
                            submission_date
                            votes {
                                email
                            }
                        }
                    }
                """

contest_submission_query_user = """
                    query TestQuery($user_email: String!) {
                        contest_submissions(user_email: $user_email) {
                            id
                            contest {
                                id
                            }
                            picture {
                                id
                                user {
                                    email
                                }
                            }
                            submission_date
                            votes {
                                email
                            }
                        }
                    }
                """

contest_submission_query_contest = """
                    query TestQuery($contest: Int!) {
                        contest_submissions(contest: $contest) {
                            id
                            contest {
                                id
                            }
                            picture {
                                id
                                user {
                                    email
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
                                email
                            }
                            picture_path
                            likes {
                                email
                            }
                        }
                    }
                """

picture_query_one = """
                    query TestQuery($picture: Int!) {
                        pictures(picture: $picture) {
                            id
                            user {
                                email
                            }
                            picture_path
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

picture_comment_query_one = """
                    query TestQuery($id: Int!) {
                        picture_comments(id: $id) {
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

picture_comment_query_user = """
                    query TestQuery($user_email: String!) {
                        picture_comments(user_email: $user_email) {
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

picture_comment_query_picture = """
                    query TestQuery($picture_id: Int!) {
                        picture_comments(picture_id: $picture_id) {
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

user_query_all = """
                    query TestQuery {
                        users {
                            email
                            name_first
                            name_last
                            profile_picture {
                                id
                            }
                            profile_picture_updated_at
                            user_handle
                        }
                    }
                """

user_query_one = """
                    query TestQuery($email: String!) {
                        users(email: $email) {
                            email
                            name_first
                            name_last
                            profile_picture {
                                id
                            }
                            profile_picture_updated_at
                            user_handle
                        }
                    }
                """
