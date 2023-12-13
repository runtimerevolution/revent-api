import strawberry
from strawberry.schema.config import StrawberryConfig

from photo.mutations import Mutation
from photo.queries import Query

schema = strawberry.Schema(
    query=Query, mutation=Mutation, config=StrawberryConfig(auto_camel_case=False)
)
