from django.shortcuts import render, redirect, reverse, HttpResponse

# Create your views here.


def view_bag(request):
    """ A view to show shopping bag """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """Adjust the quantity of product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # get bag varible if exists or create it.
    bag = request.session.get('bag', {})

    # check if product with sizes is being added
    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    # overwrite the session with updated version
    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Add a quantity of the product to bag"""

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # get bag varible if exists or create it.
    bag = request.session.get('bag', {})

    # check if bag has quanity
    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
            if not bad[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        # no quanity
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    # overwrite the session with updated version
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove item from shopping bag"""

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        # get bag varible if exists or create it.
        bag = request.session.get('bag', {})

        # Only deleting product of certain size
        if size:
            del bag[item_id]['items_by_size'][size]
            # if it was the only size the had in bag
            if not bad[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            # no size
            bag.pop(item_id)

        # overwrite the session with updated version
        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=500)
