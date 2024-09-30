
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

picture_query_all = """
    query TestQuery {
        pictures {
            id
            user {
                email
            }
            file
            description
            likes {
                id
            }
        }
    }