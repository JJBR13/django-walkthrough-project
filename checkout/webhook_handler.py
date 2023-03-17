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
            content=f'Unhandled webhooks recived: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment success webhook from stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        # clean data in shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False
        try:
            order = Order.objects.get(
                # look up exact but is NOT case sensitive
                full_name_iexact=shipping_details.name,
                email_iexact=shipping_details.email,
                phone_number_iexact=shipping_details.phone,
                country_iexact=shipping_details.country,
                postcode_iexact=shipping_details.postal_code,
                town_or_city_iexact=shipping_details.city,
                street_address1_iexact=shipping_details.line1,
                street_address2_iexact=shipping_details.line2,
                county_iexact=shipping_details.state,
                grand_total=grand_total,
            )
            order_exists = True
            return HttpResponse(
                content=f'Webhooks recived: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        except Order.DoesNotExist:
            try:
                for item_id, item_data in json.loads(bag).items():
                    order.objects.create(
                        full_name=shipping_details.name,
                        email=shipping_details.email,
                        phone_number=shipping_details.phone,
                        country=shipping_details.country,
                        postcode=shipping_details.postal_code,
                        town_or_city=shipping_details.city,
                        street_address1=shipping_details.line1,
                        street_address2=shipping_details.line2,
                        county=shipping_details.state,
                    )
                    product = Product.objects.get(id=item_id)
                    # if item is int, mean has not sizes
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        # if item has sizes
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return httpResponse(
                    content=f'Webhooks recived: {event["type"]} | ERROR: {e}',
                    status=500)

        return HttpResponse(
            content=f'Webhooks recived: {event["type"]}',
            status=200)

    def handle_payment_intent_failed(self, event):
        """
        Handle the payment fail webhook from stripe
        """
        return HttpResponse(
            content=f'Webhooks recived: {event["type"]}',
            status=200)
