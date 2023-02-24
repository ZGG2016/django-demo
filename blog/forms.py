from django import forms

from blog.models import Person


class PersonForm(forms.ModelForm):
    class Meta:
        # TODO 表明这个表单对应的数据库模型是 Person 类
        model = Person
        # TODO 表单需要显示的字段
        fields = ['name', 'gender', 'email', 'url', 'text']
