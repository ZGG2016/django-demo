
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from pure_pagination import PaginationMixin

from blog.forms import PersonForm
from blog.models import Publisher, Book, Author, Person, Reporter, Article, Publication, Article2, Person2, Group, \
    Membership
from blog.signals import PizzaStore


def test1(request, year=0, foo='foo'):
    print(year, foo)
    return HttpResponse("111111111111111")


def test2(request, foo='foo'):
    print(foo)
    return HttpResponse("222222222222")


def test3(request, foo='foo'):
    print(foo)
    return HttpResponse("3333333333333")


# TODO 类视图
class Test4(View):
    # TODO 类属性
    age = 18

    def get(self, request, name='zhangsan'):
        print("request.method --> " + request.method)
        print("name --> " + name)
        print("self.age --> " + str(self.age))
        return HttpResponse("444444444444")


# TODO 类视图 使用mixin
class Test5(TemplateView):
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['age'] = '18'
        # {'name': 'zhangsan', 'view': <blog.views.Test5 object at 0x000002180403A610>, 'sex': 'male', 'age': '18'}
        print(context)
        return context


# TODO 装饰类视图
# decorators = [never_cache, login_required]
# @method_decorator(decorators, name='dispatch')
class Test6(TemplateView):
    template_name = 'test.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# TODO 通用类视图ListView
class PublisherListView(ListView):
    template_name = 'test.html'
    context_object_name = 'my_favorite_publishers'
    model = Publisher


# TODO 通用类视图DetailView
class PublisherDetailView(DetailView):
    template_name = 'test.html'
    context_object_name = 'my_favorite_publishers'
    # model = Publisher
    queryset = Publisher.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_list'] = Book.objects.all()
        #{'object': <Publisher: zhangsan>, 'my_favorite_publishers': <Publisher: zhangsan>,
        # 'view': <blog.views.PublisherDetailView object at 0x00000134EB468370>, 'book_list': <QuerySet [<Book: Book object (1)>, <Book: Book object (2)>]>}
        print(context)
        return context


# TODO 类视图 queryset
class PublisherListView2(ListView):
    template_name = 'test.html'
    context_object_name = 'my_favorite_publishers2'
    queryset = Publisher.objects.filter(~Q(name='zhangsan')).order_by('name')


# TODO 类视图 动态过滤
class AuthorListView(ListView):
    template_name = 'test.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        self.author = get_object_or_404(Author, name=self.kwargs['author'])
        print(self.author)
        return self.author.book_set.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['author'] = self.author
        return context


# TODO 类视图 执行额外工作
class AuthorDetailView(DetailView):
    template_name = 'test.html'
    queryset = Author.objects.all()

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # 更新 last_accessed 字段
        obj.last_accessed = timezone.now()
        obj.save()
        return obj


# TODO 类视图  Using SingleObjectMixin with View
class RecordInterestView(SingleObjectMixin, View):
    model = Author

    def get(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return HttpResponseForbidden()

        self.object = self.get_object()
        # TODO 反向解析
        return HttpResponseRedirect(reverse('blog:author-detail', kwargs={'pk': self.object.pk}))


# TODO 类视图 Using SingleObjectMixin with ListView
class PublisherDetailView2(SingleObjectMixin, ListView):
    template_name = 'test.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Publisher.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publisher'] = self.object
        return context

    def get_queryset(self):
        return self.object.book_set().all()


class PersonDetailView(DetailView):
    template_name = 'test.html'
    context_object_name = 'person'
    model = Person


def show_form(request):
    return render(request, "fillinform.html")


@require_POST
def save_person(request):

    form = PersonForm(request.POST)
    # print(form)
    if form.is_valid():
        person = form.save(commit=False)
        person.save()

        messages.add_message(request, messages.SUCCESS, '保存成功！', extra_tags='success')
        return redirect(person)

    context = {'form': form}
    messages.add_message(request, messages.ERROR, '保存失败！', extra_tags='danger')

    return render(request, 'fillinform.html', context=context)


# TODO 分页api测试
def paginator_test(request):
    objects = ['john', 'paul', 'george', 'ringo']
    p = Paginator(objects, 2)
    print(p.count)  # 4
    print(p.num_pages)  # 2
    print(type(p.page_range))  # <class 'range'>
    print(p.page_range)  # range(1, 3)
    print("--------------------")

    page1 = p.page(1)
    print(page1)  # <Page 1 of 2>
    p1 = page1.object_list
    print(p1)  # ['john', 'paul']
    page2 = p.page(2)
    p2 = page2.object_list
    print(p2)  # ['george', 'ringo']
    print("--------------------")

    print(page2.has_next())  # False
    print(page2.has_previous())  # True
    print(page2.has_other_pages())  # True
    # print(page2.next_page_number())  # 报错 django.core.paginator.EmptyPage: 本页结果为空
    print(page2.previous_page_number())  # 1
    print(page2.start_index())  # 3
    print(page2.end_index())  # 4

    # print(p.page(0))  # 报错 django.core.paginator.EmptyPage: 页码小于 1
    # print(p.page(3))  # 报错 django.core.paginator.EmptyPage: 本页结果为空
    return HttpResponse("paginator_test")


# TODO 分页 ListView 测试
class PagListView(ListView):
    template_name = 'test.html'
    context_object_name = 'author_list'
    paginate_by = 2
    model = Author


# TODO 分页 函数视图 测试
def paglisting(request):
    author_list = Author.objects.all()
    paginator = Paginator(author_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'test.html', {'page_obj': page_obj})


# TODO django-pure-pagination 分页
class PagListView2(PaginationMixin, ListView):
    template_name = 'test.html'
    # context_object_name = 'author_list'
    paginate_by = 2
    model = Author


# TODO 自定义信号
def test_signal(request):
    ps = PizzaStore(addr="beijing")
    ps.send_pizza()

    return HttpResponse("test_signal............")










