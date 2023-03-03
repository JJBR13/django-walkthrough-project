from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """ A view to show shopping bag """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """Add a quantity of the product to bag"""

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    # get bag varible if exists or create it.
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        # update the quantity if already exists 
        bag[item_id] += quantity
    else:
        # add the item to the bag
        bag[item_id] = quantity

    # overwrite the session with updated version
    request.session['bag'] = bag
    return redirect(redirect_url)
