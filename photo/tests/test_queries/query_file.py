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

collections_query_one = """
                    query TestQuery($id: Int!) {
                        collections(id: $id) {
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

collections_query_user_name = """
                    query TestQuery($user: UUID!, $name: String!) {
                        collections(user: $user, name: $name) {
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

collections_query_user = """
                    query TestQuery($user: UUID!) {
                        collections(user: $user) {
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

collections_query_name = """
                    query TestQuery($name: String!) {
                        collections(name: $name) {
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

picture_query_all = """
                    query TestQuery {
                        pictures {
                            id
                            user {
                                email
                            }
                            file
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
                    query TestQuery($user: UUID!) {
                        picture_comments(user: $user) {
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
