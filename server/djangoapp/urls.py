from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path(route='', view=views.get_dealerships, name='index'),
    path(route='dealership', view=views.get_dealership, name='dealership'),
    path(route='dealership/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),
    path(route='contact', view=views.contact_us, name='contact'),
    path(route='about', view=views.about_us, name='about'),
    path(route='login', view=views.login_request, name='login'),
    path(route='logout', view=views.logout_request, name='logout'),
    path(route='registration', view=views.registration_request, name='registration'),
    path(route='add_review', view=views.add_review, name='add_review'),
    path(route='add_review/<int:dealer_id>/', view=views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)