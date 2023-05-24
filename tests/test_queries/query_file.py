# File with the queries used by the tests

collections_query_all = """
                            query TestQuery {
                                collections {
                                    name
                                    user {
                                        email
                                    }
                                    pictures {
                                        picture_path
                                    }
                                }
                            }
                        """

collections_query_one = """
                    query TestQuery($user_email: String!, $name: String!) {
                        collections(user_email: $user_email, name: $name) {
                            name
                            user {
                                email
                                name_first
                                name_last
                            }
                            pictures {
                                picture_path
                            }
                        }
                    }
                """

collections_query_user = """
                    query TestQuery($user_email: String!) {
                        collections(user_email: $user_email) {
                            name
                            user {
                                email
                                name_first
                                name_last
                            }
                            pictures {
                                picture_path
                            }
                        }
                    }
                """

collections_query_name = """
                    query TestQuery($name: String!) {
                        collections(name: $name) {
                            name
                            user {
                                email
                                name_first
                                name_last
                            }
                            pictures {
                                picture_path
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
                                picture_path
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
                                picture_path
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
                                picture_path
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
                                picture_path
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
                            user {
                                email
                                name_first
                                name_last
                            }
                            picture_path
                            likes {
                                email
                            }
                        }
                    }
                """

picture_query_one = """
                    query TestQuery($picture_path: String!) {
                        pictures(picture_path: $picture_path) {
                            user {
                                email
                                name_first
                                name_last
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
                            user {
                                email
                            }
                            picture {
                                picture_path
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
                                picture_path
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
                                picture_path
                            }
                            text
                            created_at
                        }
                    }
                """

picture_comment_query_picture = """
                    query TestQuery($picture_path: String!) {
                        picture_comments(picture_path: $picture_path) {
                            id
                            user {
                                email
                            }
                            picture {
                                picture_path
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
                                picture_path
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
                                picture_path
                            }
                            profile_picture_updated_at
                            user_handle
                        }
                    }
                """
