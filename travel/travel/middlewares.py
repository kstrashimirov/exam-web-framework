from travel.web.views import InternalErrorView, Internal404ErrorView


def handle_exception(get_response):
    def middleware(request):
        response = get_response(request)
        if response.status_code == 404:
            return Internal404ErrorView.as_view()(request)

        elif response.status_code > 400 and response.status_code != 404:
            return InternalErrorView.as_view()(request)

        return response

    return middleware
