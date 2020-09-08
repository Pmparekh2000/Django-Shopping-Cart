from .cart import Cart

def cart(request):
    return {'cart': Cart(request)}
    # In context processors we get the request object as a parameter
    # and return a dictionary of objects that will be available to all 
    # templates rendered using "RequestContext"
