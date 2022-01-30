from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    path(route='about/', view=views.about_page, name='about_us'),

    path(route='contact/', view=views.contact_page, name='contact_us'),

    path(route='register/', view=views.registration_page, name='register_account'),

    path(route='login/', view=views.login_request, name='login'),

    path(route='logout/', view=views.logout_request, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),

    path(route='reviews/<str:dealership_id>', view=views.get_dealer_details, name='reviews'),

    path(route='reviews/add/new/', view=views.add_review, name='add_review'),

    path(route='reviews/add/<str:car_year>/<str:car_make>/<str:car_model>/<str:purchase_date>/<str:dealership_review>/<str:dealership>/<str:sentiment>', view=views.add_review, name='add_review')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)