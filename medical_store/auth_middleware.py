from django.shortcuts import redirect


class UserAuthenticate:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request, eml=None):

        if not request.session.get('login'):
            return redirect('/')
        response = self.get_response(request)
        return response

