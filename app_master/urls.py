from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.home, name='home'),
    path('inputideas', views.inputideas_form, name='form'),
    path('idea_success', views.idea_success, name='idea_success'),
    

    path('list', views.idea_list, name='list'),
    # path('ideas',views.all_ideas,name='list'),
    path('update/<int:id>', views.idea_update, name='update'),
    path('about', views.about, name='about'),
    path('feedback', views.feedback, name='feedback'),
    path('feedback_success', views.feedback_success, name='feedback_success'),
    path('disclaimer_seen', views.disclaimer_seen, name='disclaimer_seen'),
    path('howto', views.how_to, name = "howto"),
    
    path('ideas/', views.display_ideas, name='list'),
    path('ideas/<str:town>/', views.get_summaries, name='get_summaries'),



    # path('idea/',include('app_master.urls'))
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
