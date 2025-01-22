from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, LoginView, RegisterView

router = DefaultRouter()
router.register('items', ItemViewSet)

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('', include(router.urls))
]
