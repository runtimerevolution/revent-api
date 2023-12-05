from django.http import HttpRequest, HttpResponse
from photo.queries import Context
from strawberry.django.views import GraphQLView


class ReventGraphQLView(GraphQLView):
    def get_context(self, request, response: HttpResponse) -> any:
        context = Context()
        context.request = request
        return context
