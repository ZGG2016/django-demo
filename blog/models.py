from django.db import models
from django.urls import reverse
from django.utils import timezone


class Publisher(models.Model):
    # TODO 指定自增primary key的类型  表范围
    # id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    class Meta:
        ordering = ["-name"]
        # TODO 数据库中对应的表名，默认情况下是 appname_modelname，如blog_publisher
        db_table = "publishers"

    # TODO 反向解析
    def get_absolute_url(self):
        return reverse("blog:author-detail", kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Author(models.Model):
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='author_headshots')
    last_accessed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(
        Author,
        verbose_name='list of authors')


# -------------------------------------------------------------
# TODO  model不同字段类型 不同选项 对应的html组件的表现
class Person(models.Model):
    name = models.CharField('姓名', max_length=50)
    gender = models.CharField('性别', max_length=50, default='', choices=[('男', 'man'), ('女', 'woman')])
    email = models.EmailField('邮箱', default='123@qq.com')
    url = models.URLField('个人地址', blank=True)
    text = models.TextField('内容', default='', help_text='随便写点')
    login_time = models.DateTimeField('登录时间', default=timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:person-info", kwargs={'pk': self.pk})


# -------------------------------------------------------------
# TODO MODEL 多对一关系
class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE, verbose_name='reporter')

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ['headline']


# -------------------------------------------------------------
# TODO MODEL 多对多关系
class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Article2(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ['headline']

    def __str__(self):
        return self.headline


class Person2(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person2, through='Membership')

    def __str__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(Person2, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)


# -------------------------------------------------------------
# TODO MODEL 一对一关系
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return "%s the place" % self.name


class Restaurant(models.Model):
    place = models.OneToOneField(
                    Place,
                    on_delete=models.CASCADE,
                    related_name="restaurant",
                    primary_key=True,
                    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return "%s the restaurant" % self.place.name


class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s the waiter at %s" % (self.name, self.restaurant)


# -------------------------------------------------------------
# TODO 单元测试
class Animal(models.Model):
    name = models.CharField(max_length=50)
    sound = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def speak(self):
        return "The %s says %s" % (self.name, self.sound)
