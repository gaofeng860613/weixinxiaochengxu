from django.urls import path, include
import juheapp.views

urlpatterns = [
    path('juhe/', juheapp.views.hello_juhe),
    path('testrequest/', juheapp.views.testrequest),
    path('image/', juheapp.views.image),
    path('apps/', juheapp.views.apps),
    path('image1/', juheapp.views.image1),
    path('imageclass/', juheapp.views.imageView.as_view()),
    path('wenben/', juheapp.views.wenben),
    path('test_mixin/', juheapp.views.test_mixin.as_view()),
    path('loaderupdown/', juheapp.views.loader_up_down_pic.as_view()),
    path('cookietest/', juheapp.views.CookieTest.as_view()),
    path('cookietest2/', juheapp.views.CookieTest2.as_view()),
    path('userview/', juheapp.views.UserView.as_view()),
    path('focusdata/', juheapp.views.focus_data.as_view()),
    path('logout/', juheapp.views.LogOut.as_view()),
    path('userstatus/', juheapp.views.UserStatus.as_view()),
    path('weather/', juheapp.views.Weather.as_view()),
]