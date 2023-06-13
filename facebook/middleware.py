from django.shortcuts import redirect
from django.urls import reverse
from core.models import Profile

class ProfileCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_anonymous:
            profile = Profile.objects.filter(user=request.user).first()
            if not profile:
                if request.path != reverse('core:create-profile'):
                    return redirect('core:create-profile')

        response = self.get_response(request)
        return response
