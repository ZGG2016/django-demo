
from django.core.signals import request_finished
from django.db.models.signals import pre_save
from django.dispatch import receiver, Signal
from blog.models import Person

# TODO 信号处理器通常定义在应用程序下的单独的一个子模块(signals)下
#      connect函数定义在应用程序配置类的ready方法中，


# TODO 方法2：通过receiver装饰器注册一个信号接收函数（信号处理器），每当一个HTTP请求完成时，就会调用my_callback回调函数
@receiver(request_finished, dispatch_uid="request_finished unique uid method2")
# TODO 所有的信号处理器都必须指定这两个参数
def my_callback(sender, **kwargs):
    print("request finished......")


# TODO Person模型保存一条数据前，执行这个函数
@receiver(pre_save, sender=Person)
def my_callback2(sender, **kwargs):
    print("将要保存一条Person数据")


# TODO 自定义信号
pizza_done = Signal()


class PizzaStore:
    def __init__(self, addr = "chengdu"):
        self.addr = addr

    def send_pizza(self):
        pizza_done.send(self.__class__)


@receiver(pizza_done, sender=PizzaStore)
def my_callback3(sender, **kwargs):
    print("pizza发出......")
