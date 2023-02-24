from django.apps import AppConfig


class BlogConfig(AppConfig):
    # TODO 指定自增primary key的类型  app范围
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
