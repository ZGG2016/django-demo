from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path, include
from django.views.generic import TemplateView

from blog import views, views_model
from blog.views import Test4, Test5, Test6, PublisherListView, PublisherDetailView, PublisherListView2, \
    AuthorListView, AuthorDetailView, RecordInterestView, PersonDetailView, PagListView, PagListView2

app_name = 'blog'
urlpatterns = [
    path('1/', views.test1),
    path('<int:year>/', views.test1, {'foo': 'bar'}),

    path('<str:name>/', Test4.as_view()),
    # path('<str:name>/', Test4.as_view(age=20))

    path('2/<str:name>/', Test5.as_view(extra_context={'sex': 'male'})),

    # path('3/', login_required(TemplateView.as_view(template_name="test.html"))),
    # path('4/', permission_required('polls.can_vote')(Test5.as_view())),

    path('5/', Test6.as_view()),

    # TODO 类试图
    path('6/publishers/', PublisherListView.as_view()),
    path('7/publishers/<int:pk>/', PublisherDetailView.as_view()),
    path('8/publishers/', PublisherListView2.as_view()),
    path('9/<str:author>/', AuthorListView.as_view()),

    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),

    path('author/<int:pk>/interest/', RecordInterestView.as_view(), name='author-interest'),

    # TODO  1.表单使用  2.model不同字段类型对应的html组件
    path('person/1/', views.show_form),
    path('person/2/', views.save_person, name='person-form'),
    path('person/1/<int:pk>/', PersonDetailView.as_view(), name='person-info'),

    path('manytoone/1/', views_model.many_to_one_test),
    path('manytomany/1/', views_model.many_to_many_test),
    path('manytomany/2/', views_model.many_to_many_test2),
    path('onetoone/1/', views_model.one_to_one_test),

    # TODO 分页
    path('paginator/1/', views.paginator_test),
    path('paginator/2/', PagListView.as_view()),
    path('paginator/3/', views.paglisting),
    path('paginator/4/', PagListView2.as_view()),

    # TODO 自定义信号
    path('signal/1/', views.test_signal)
]
