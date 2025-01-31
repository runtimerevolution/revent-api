from django.http import HttpResponse
from strawberry.django.views import GraphQLView

from photo.queries import Context, Query


class ReventGraphQLView(GraphQLView):
    def get_context(self, request, response: HttpResponse) -> any:
        context = Context()
        context.request = request
        return context
