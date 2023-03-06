from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """ A view to show shopping bag """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """Add a quantity of the product to bag"""

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
