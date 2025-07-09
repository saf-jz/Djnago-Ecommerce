from cart.models import Cart
def count_items(request):
    if request.user.is_authenticated: # if user is logged in
        u=request.user
        c=Cart.objects.filter(user=u)
        count=0
        for i in c:
            count+=i.quantity #calculate the no of items in the cart
    else:
        count=0

    return {'count':count}