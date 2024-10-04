from django.shortcuts import redirect
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.views import SpectacularSwaggerView


# class CustomAuthenticationScheme(OpenApiAuthenticationExtension):
#     target_class = 'users.authenticate.CustomAuthentication'  # full import path to your authentication class
#     name = 'CustomAuth'  # name of the scheme used in the OpenAPI schema
#
#     def get_security_definition(self, auto_schema):
#         return {
#             'type': 'http',  # or 'apiKey', 'oauth2', etc.
#             'scheme': 'bearer',  # replace with the scheme you are using, e.g., 'basic', 'bearer'
#             'bearerFormat': 'JWT',  # if you're using JWTs, or customize as needed
#         }
#
# # Register the extension with drf-spectacular automatically when it's loaded


class CustomSpectacularSwaggerView(SpectacularSwaggerView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)