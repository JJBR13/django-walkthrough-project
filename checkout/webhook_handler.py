from django.http import HttpResponse


class StripeWH_Handler:
    """
    Handle Stripe webhooks
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknow/unexpected webhook event
        """
        return HttpResponse(
            content=f'Webhooks recived: {event["type"]}',
            status=200)
