from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.


def view_bag(request):
    """ A view to show shopping bag """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """Adjust the quantity of product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
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
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
            else:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    # overwrite the session with updated version
    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Add a quantity of the product to bag"""

    product = get_object_or_404(Product, pk=item_id)
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
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
        else:
            del bag[item_id]['items_by_size'][size]
            if not bad[item_id]['items_by_size']:
                bag.pop(item_id)
                messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')

    else:
        # no quanity
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')

        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    # overwrite the session with updated version
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove item from shopping bag"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        # get bag varible if exists or create it.
        bag = request.session.get('bag', {})

        # Only deleting product of certain size
        if size:
            del bag[item_id]['items_by_size'][size]
            # if it was the only size the had in bag
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')

        else:
            # no size
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        # overwrite the session with updated version
        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        print(e)
        return HttpResponse(status=500)
