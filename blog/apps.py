from django.apps import AppConfig
from django.core.signals import request_finished


class BlogConfig(AppConfig):
    # TODO 指定自增primary key的类型  app范围
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        # TODO 采用方法2，必须添加这条语句， Implicitly connect signal handlers decorated with @receiver.
        from blog import signals
        # TODO 方法1：通过connect注册一个信号接收函数（信号处理器），每当一个HTTP请求完成时（也就是request_finished信号发送时），就会调用my_callback回调函数
        #      也就是将发送的信号和接收器连接起来
        #      dispatch_uid防止接收器函数运行多次
        #      Explicitly connect a signal handler.
        # request_finished.connect(signals.my_callback, dispatch_uid="request_finished unique uid method1")

