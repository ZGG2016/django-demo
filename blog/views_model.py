from datetime import date

from django.http import HttpResponse

from blog.models import Reporter, Article, Publication, Article2, Person2, Group, Membership, Place, Restaurant, Waiter


# TODO MODEL 多对一关系
def many_to_one_test(request):
    print("============ many_to_one_test =============")
    Reporter.objects.all().delete()
    Article.objects.all().delete()

    r1 = Reporter(first_name='John', last_name='Smith', email='john@example.com')
    r1.save()
    r2 = Reporter(first_name='Paul', last_name='Jones', email='paul@example.com')
    r2.save()

    # 直接new一个Article对象，必须先创建好r1对象
    a = Article(id=None, headline='this is a test', pub_date=date(2022, 11, 11), reporter=r1)
    a.save()

    print(a.id)
    print(a.reporter)  # John Smith
    print(a.reporter.id)
    print(a.reporter.first_name + " " +a.reporter.last_name)  # John Smith
    print("---------")

    r = a.reporter

    # 通过Reporter对象间接创建Article对象
    a2 = r.article_set.create(headline="John's second story", pub_date=date(2022, 12, 12))
    print(a2)  # John's second story
    print(a2.id)
    print(a2.reporter)  # John Smith
    print(a2.reporter.id)
    print("---------")

    # 通过Reporter对象直接创建Article对象
    a3 = Article.objects.create(headline="Paul's story", pub_date=date(2022, 10, 17), reporter=r)
    print(a3.reporter)  # John Smith
    # r对应的文章
    # <QuerySet [<Article: John's second story>, <Article: Paul's story>, <Article: this is a test>]>
    print(r.article_set.all())
    print("---------")

    # "Paul's story 从 John 移动到 Paul
    r2.article_set.add(a3)
    print(a3.reporter)  # Paul Jones
    print(r.article_set.all())  # <QuerySet [<Article: John's second story>, <Article: this is a test>]>
    print(r2.article_set.all())  # <QuerySet [<Article: Paul's story>]>
    print(r.article_set.count())  # 2
    print(r2.article_set.count())  # 1
    print("-------------")

    f1 = r.article_set.filter(headline__startswith="this")
    print(f1)  # <QuerySet [<Article: this is a test>]>
    f2 = Article.objects.filter(reporter__first_name="John")
    print(f2)  # <QuerySet [<Article: John's second story>, <Article: this is a test>]>
    f3 = Article.objects.filter(reporter__first_name="John", reporter__last_name="Smith")
    print(f3)  # <QuerySet [<Article: John's second story>, <Article: this is a test>]>
    f4 = Article.objects.filter(reporter__pk=1)
    print(f4)
    f5 = Article.objects.filter(reporter=1)
    print(f5)
    f6 = Article.objects.filter(reporter=r)
    print(f6)  # <QuerySet [<Article: John's second story>, <Article: this is a test>]>
    f7 = Article.objects.filter(reporter__in=[1, 2]).distinct()
    print(f7)
    f8 = Article.objects.filter(reporter__in=[r, r2]).distinct()
    print(f8)  # <QuerySet [<Article: John's second story>, <Article: Paul's story>, <Article: this is a test>]>
    f9 = Article.objects.filter(reporter__in=Reporter.objects.filter(first_name="John")).distinct()
    print(f9)  # <QuerySet [<Article: John's second story>, <Article: this is a test>]>
    print("-------------")

    f10 = Reporter.objects.filter(article__pk=1)
    print(f10)
    f11 = Reporter.objects.filter(article=1)
    print(f11)
    f12 = Reporter.objects.filter(article=a)
    print(f12)  # <QuerySet [<Reporter: John Smith>]>
    f13 = Reporter.objects.filter(article__headline__startswith="this")
    print(f13)  # <QuerySet [<Reporter: John Smith>]>
    f14 = Reporter.objects.filter(article__headline__startswith="this").distinct()
    print(f14)  # <QuerySet [<Reporter: John Smith>]>
    f15 = Reporter.objects.filter(article__headline__startswith="this").count()
    print(f15)  # 1
    f16 = Reporter.objects.filter(article__headline__startswith="this").distinct().count()
    print(f16)  # 1
    print("-------------")

    f17 = Reporter.objects.filter(article__reporter__first_name="John")
    print(f17)  # <QuerySet [<Reporter: John Smith>, <Reporter: John Smith>]>
    f18 = Reporter.objects.filter(article__reporter__first_name="John").distinct()
    print(f18)  # <QuerySet [<Reporter: John Smith>]>
    f19 = Reporter.objects.filter(article__reporter=r).distinct()
    print(f19)  # <QuerySet [<Reporter: John Smith>]>
    print("-------------")

    a_all1 = Article.objects.all()
    print(a_all1)  # <QuerySet [<Article: John's second story>, <Article: Paul's story>, <Article: this is a test>]>
    r_all1 = Reporter.objects.order_by("first_name")
    print(r_all1)  # <QuerySet [<Reporter: John Smith>, <Reporter: Paul Jones>]>
    r2.delete()
    a_all2 = Article.objects.all()
    print(a_all2)  # <QuerySet [<Article: John's second story>, <Article: this is a test>]>
    r_all2 = Reporter.objects.order_by("first_name")
    print(r_all2)  # <QuerySet [<Reporter: John Smith>]>
    Reporter.objects.filter(article__headline__startswith='This').delete()
    a_all3 = Article.objects.all()
    print(a_all3)
    r_all3 = Reporter.objects.order_by("first_name")
    print(r_all3)
    return HttpResponse("many_to_one_test")


# TODO MODEL 多对多关系
def many_to_many_test(request):
    print("============ many_to_many_test =============")
    Publication.objects.all().delete()
    Article2.objects.all().delete()

    p1 = Publication(title='The Python Journal')
    p1.save()
    p2 = Publication(title='Science News')
    p2.save()
    p3 = Publication(title='Science Weekly')
    p3.save()
    a1 = Article2(headline='Django lets you build web apps easily')
    a1.save()
    # 必须先执行 a1.save()
    a1.publications.add(p1)
    print(a1)  # Django lets you build web apps easily
    print("-----------------")

    a2 = Article2(headline='NASA uses Python')
    a2.save()
    a2.publications.add(p1, p2)
    a2.publications.add(p3)
    print(a2)
    # 可以再次添加，但不会去重
    a2.publications.add(p3)
    print(a2)
    print("-----------------")

    a2.publications.create(title='Highlights for Children')
    print("-----------------")

    # Article2对象访问它的Publication对象
    a1p = a1.publications.all()
    print(a1p)  # <QuerySet [<Publication: The Python Journal>]>
    a2p = a2.publications.all()
    # <QuerySet [<Publication: Highlights for Children>, <Publication: Science News>,
    # <Publication: Science Weekly>, <Publication: The Python Journal>]>
    print(a2p)
    print("-----------------")

    # Publication对象访问它的Article2对象
    p2a = p2.article2_set.all()
    print(p2a)  # <QuerySet [<Article2: NASA uses Python>]>
    p1a = p1.article2_set.all()
    print(p1a)  # <QuerySet [<Article2: Django lets you build web apps easily>, <Article2: NASA uses Python>]>
    # pid = Publication.objects.get(id=4).article2_set.all()
    # print(pid)
    print("-----------------")

    # 查询
    # qa1 = Article2.objects.filter(publications__id=1)
    # qa2 = Article2.objects.filter(publications__pk=1)
    # qa3 = Article2.objects.filter(publications=1)
    qa4 = Article2.objects.filter(publications=p1)
    qa5 = Article2.objects.filter(publications__title__startswith="Science")
    print(qa5)  # <QuerySet [<Article2: NASA uses Python>, <Article2: NASA uses Python>]>
    qa6 = Article2.objects.filter(publications__title__startswith="Science").distinct()
    print(qa6)  # <QuerySet [<Article2: NASA uses Python>]>
    # qa7 = Article2.objects.filter(publications__in=[1, 2]).distinct()
    qa8 = Article2.objects.filter(publications__in=[p1, p2]).distinct()
    print(qa8)  # <QuerySet [<Article2: Django lets you build web apps easily>, <Article2: NASA uses Python>]>
    qa9 = Article2.objects.filter(publications__title__startswith="Science").count()
    print(qa9)  # 2
    qa10 = Article2.objects.filter(publications__title__startswith="Science").distinct().count()
    print(qa10)  # 1
    qa11 = Article2.objects.exclude(publications=p2)
    print(qa11)  # <QuerySet [<Article2: Django lets you build web apps easily>]>
    print("-----------------")

    # 反向查询
    # qp1 = Publication.objects.filter(pk=1)
    qp2 = Publication.objects.filter(article2__headline__startswith="NASA")
    # <QuerySet [<Publication: Highlights for Children>, <Publication: Science News>,
    # <Publication: Science Weekly>, <Publication: The Python Journal>]>
    print(qp2)
    # qp3 = Publication.objects.filter(article2__id=1)
    # qp4 = Publication.objects.filter(article2__pk=1)
    # qp5 = Publication.objects.filter(article2=1)
    # qp6 = Publication.objects.filter(article2=a1)
    # qp7 = Publication.objects.filter(article2__in=[1, 2]).distinct()
    qp8 = Publication.objects.filter(article2__in=[a1, a2]).distinct()
    # <QuerySet [<Publication: Highlights for Children>, <Publication: Science News>,
    # <Publication: Science Weekly>, <Publication: The Python Journal>]>
    print(qp8)
    print("-----------------")

    # 删除
    p1.delete()
    dp1 = Publication.objects.all()
    # <QuerySet [<Publication: Highlights for Children>, <Publication: Science News>, <Publication: Science Weekly>]>
    print(dp1)
    dp2 = a1.publications.all()
    print(dp2)  # <QuerySet []>

    a2.delete()
    da1 = Article2.objects.all()
    print(da1)  # <QuerySet [<Article2: Django lets you build web apps easily>]>
    da2 = p2.article2_set.all()
    print(da2)  # <QuerySet []>

    # 反向添加
    a4 = Article2(headline="NASA finds intelligent life on Earth")
    a4.save()
    p2.article2_set.add(a4)
    p2a4 = p2.article2_set.all()
    print(p2a4)  # <QuerySet [<Article2: NASA finds intelligent life on Earth>]>
    a4h = a4.publications.all()
    print(a4h)  # <QuerySet [<Publication: Science News>]>
    print("-----------------")

    new_article = p2.article2_set.create(headline="Oxygen-free diet works wonders")
    p2new = p2.article2_set.all()
    # <QuerySet [<Article2: NASA finds intelligent life on Earth>, <Article2: Oxygen-free diet works wonders>]>
    print(p2new)
    a5 = p2.article2_set.all()[1]
    a5h = a5.publications.all()
    # <QuerySet [<Publication: Science News>]>
    print(a5h)
    print("-----------------")

    # 移除
    # a4.publications.remove(p2)
    # p2a4 = p2.article2_set.all()
    # print(p2a4)  # <QuerySet [<Article2: Oxygen-free diet works wonders>]>
    # a4h = a4.publications.all()
    # print(a4h)  # <QuerySet []>

    p2.article2_set.remove(a5)
    p2a5 = p2.article2_set.all()
    print(p2a5)  # <QuerySet []>
    a5h = a5.publications.all()
    print(a5h)  # <QuerySet []>
    print("-----------------")

    a4p = a4.publications.all()
    print(a4p)  # <QuerySet [<Publication: Science News>]>
    a4.publications.set([p3])
    a4p = a4.publications.all()
    print(a4p)  # <QuerySet [<Publication: Science Weekly>]>
    print("-----------------")

    # 清除
    p2.article2_set.clear()
    p2a = p2.article2_set.all()
    print(p2a)  # <QuerySet []>

    p2.article2_set.add(a4, a5)
    p2a = p2.article2_set.all()
    # <QuerySet [<Article2: NASA finds intelligent life on Earth>, <Article2: Oxygen-free diet works wonders>]>
    print(p2a)
    a4p = a4.publications.all()
    print(a4p)  # <QuerySet [<Publication: Science News>, <Publication: Science Weekly>]>
    a4.publications.clear()
    p2a = p2.article2_set.all()
    print(p2a)  # <QuerySet [<Article2: Oxygen-free diet works wonders>]>
    a4p = a4.publications.all()
    print(a4p)  # <QuerySet []>
    print("-----------------")

    p1 = Publication(title='The Python Journal')
    p1.save()
    a2 = Article2(headline='NASA uses Python')
    a2.save()
    a2.publications.add(p1, p2, p3)
    # 批量删除
    Publication.objects.filter(title__startswith="Science").delete()
    p = Publication.objects.all()
    print(p)  # <QuerySet [<Publication: Highlights for Children>, <Publication: The Python Journal>]>
    a = Article2.objects.all()
    # <QuerySet [<Article2: Django lets you build web apps easily>, <Article2: NASA finds intelligent life on Earth>,
    #            <Article2: NASA uses Python>, <Article2: Oxygen-free diet works wonders>]>
    print(a)
    a2p = a2.publications.all()
    print(a2p)  # <QuerySet [<Publication: The Python Journal>]>

    # After the delete(), the QuerySet cache needs to be cleared, and the referenced objects should be gone
    q = Article.objects.filter(headline__startswith='Django')
    q.delete()
    print(q)  # <QuerySet []>
    p1a = p1.article2_set.all()
    print(p1a)  # <QuerySet [<Article2: NASA uses Python>]>
    return HttpResponse("many_to_many_test")


# TODO MODEL 多对多关系  关系表
def many_to_many_test2(request):
    Group.objects.all().delete()
    Person2.objects.all().delete()
    Membership.objects.all().delete()

    ringo = Person2.objects.create(name="Ringo Starr")
    paul = Person2.objects.create(name="Paul McCartney")
    beatles = Group.objects.create(name="The Beatles")
    # 通过关系表建立联系
    m1 = Membership(person=ringo, group=beatles,
                    date_joined=date(1962, 8, 16),
                    invite_reason="Needed a new drummer.")
    m1.save()

    b = beatles.members.all()
    print(b)  # <QuerySet [<Person2: Ringo Starr>]>
    rg = ringo.group_set.all()
    print(rg)  # <QuerySet [<Group: The Beatles>]>

    Membership.objects.create(person=paul, group=beatles,
                              date_joined=date(1960, 8, 1),
                              invite_reason="Wanted to form a band.")
    b2 = beatles.members.all()
    print(b2)  # <QuerySet [<Person2: Ringo Starr>, <Person2: Paul McCartney>]>

    john = Person2.objects.create(name="John McCartney")
    # Method 'add' cant be used with many-to-many relations if intermediate model is used.
    # consider call it on intermediate model manager.
    # beatles.members.add(john, through_defaults={'date_joined': date(1960, 8, 1)})
    # beatles.members.create(name="George Harrison", throught_defaults={'date_joined':date(1960, 8, 1)})
    beatles.members.set([john, paul, ringo], through_defaults={'date_joined': date(1960, 8, 1)})
    b3 = beatles.members.all()
    print(b3)  # <QuerySet [<Person2: Ringo Starr>, <Person2: Paul McCartney>, <Person2: John McCartney>]>
    print("-------------------")

    # 允许重复
    # Membership.objects.create(person=ringo, group=beatles,
    #                           date_joined=date(1968, 9, 4),
    #                           invite_reason="You've been gone for a month and we miss you.")
    # b3 = beatles.members.all()
    # # <QuerySet [<Person2: Ringo Starr>, <Person2: Paul McCartney>, <Person2: John McCartney>, <Person2: Ringo Starr>]>
    # print(b3)
    # beatles.members.remove(ringo)
    # b3 = beatles.members.all()
    # # <QuerySet [<Person2: Paul McCartney>, <Person2: John McCartney>]>
    # print(b3)
    #
    # # 清除所有的关系
    # beatles.members.clear()
    # m = Membership.objects.all()
    # print(m)  # <QuerySet []>
    # print("-------------------")

    # 查询
    g = Group.objects.filter(members__name__startswith="Paul")
    print(g)  # <QuerySet [<Group: The Beatles>]>
    # 1961.1.1后加入Beatles的成员
    p = Person2.objects.filter(group__name="The Beatles",
                               membership__date_joined__gt=date(1961, 1, 1))
    print(p)  # <QuerySet [<Person2: Ringo Starr>]>
    # 使用关系表查询成员信息
    ringos_membership = Membership.objects.get(person=ringo, group=beatles)
    print(ringos_membership.date_joined)  # 1962-08-16
    print(ringos_membership.invite_reason)  # Needed a new drummer.
    # 反向查询
    ringos_membership =ringo.membership_set.get(group=beatles)
    print(ringos_membership.date_joined)  # 1962-08-16
    print(ringos_membership.invite_reason)  # Needed a new drummer.
    return HttpResponse("many_to_many_test")


# TODO MODEL 一对一关系
def one_to_one_test(request):
    print("============== one_to_one_test =================")
    Place.objects.all().delete()
    Restaurant.objects.all().delete()
    Waiter.objects.all().delete()

    p1 = Place(name='Demon Dogs', address='944 W. Fullerton')
    # 必须先保存
    p1.save()
    p2 = Place(name='Ace Hardware', address='1013 N. Ashland')
    p2.save()

    r = Restaurant(place=p1, serves_hot_dogs=True, serves_pizza=True)
    r.save()
    print(r.place)  # Demon Dogs the place
    print(p1.restaurant)  # Demon Dogs the restaurant
    print("---------------")

    # 这会再创建一条数据
    r.place = p2
    r.save()
    print(r.place)  # Ace Hardware the place
    print(p2.restaurant)  # Ace Hardware the restaurant

    p1.restaurant = r
    print(p1.restaurant)  # Demon Dogs the restaurant
    print("---------------")

    # 查询
    r1 = Restaurant.objects.get(place=p1)
    print(r1)  # Demon Dogs the restaurant
    # Restaurant.objects.get(place_id=1)
    r2 = Restaurant.objects.filter(place__name__startswith="Demon")
    print(r2)  # <QuerySet [<Restaurant: Demon Dogs the restaurant>]>
    r3 = Restaurant.objects.exclude(place__address__contains="Ashland")
    print(r3)  # <QuerySet [<Restaurant: Demon Dogs the restaurant>]>
    print("---------------")

    # 反向查询
    # Place.objects.get(pk=1)
    pp1 = Place.objects.get(restaurant__place=p1)
    print(pp1)  # Demon Dogs the place
    pp2 = Place.objects.get(restaurant=r)
    print(pp2)  # Demon Dogs the place
    pp3 = Place.objects.get(restaurant__place__name__startswith="Demon")
    print(pp3)  # Demon Dogs the place
    print("---------------")

    w = r.waiter_set.create(name="Joe")
    print(w)  # Joe the waiter at Demon Dogs the restaurant
    pp1 = Waiter.objects.filter(restaurant__place=p1)
    print(pp1)  # <QuerySet [<Waiter: Joe the waiter at Demon Dogs the restaurant>]>
    pp2 = Waiter.objects.filter(restaurant__place__name__startswith="Demon")
    print(pp2)  # <QuerySet [<Waiter: Joe the waiter at Demon Dogs the restaurant>]>
    return HttpResponse("one_to_one_test")
