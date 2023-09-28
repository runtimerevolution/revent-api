# File with the queries used by the tests

user_query_all = """
                    query TestQuery {
                        users {
                            id
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
                    query TestQuery($user: UUID!) {
                        users(user: $user) {
                            email
                        }
                    }
                """

user_query_email = """
                    query TestQuery($email: String!) {
                        users(email: $email) {
                            id
                        }
                    }
                """
