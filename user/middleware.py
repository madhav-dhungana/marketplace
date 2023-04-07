
from django.shortcuts import redirect




class CheckUserTypeMiddleware:
    """
     middleware to check whether a user has role or not 
     When you login with google or social account , initially user don't get to choose role
     So when they are registered , they are made to choose role
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user        
        response = self.get_response(request)
        if not user.is_authenticated:
            return response
            
        if not user.role:
            if  request.path != "/user/choose-type/":
                return redirect('ChooseUserType')
        return response



