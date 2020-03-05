from django.test import TestCase

# Create your tests here.


import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'fivth_django.settings'
django.setup()

# from juheapp.models import User
# r = User.objects.filter(nickname__contains='勋')
# rr = User.objects.get(nickname='邢培勋')
# print(r,rr)



#关系映射
# Django表达三种关系映射

# - 一对一 OneToOneField
# - 一对多(多对一): ForeignKey
# - 多对多:ManyToManyField

# from django.db import models
#
# class Wife(models.Model):
#     pass
#
# class Husband(models.Model):
#     wife = models.OneToOneField(Wife, on_delete=models.CASCADE)
#
# class Mother(models.Model):
#     pass
#
# class Father(models.Model):
#     wife = models.OneToOneField(Mother,on_delete=models.DO_NOTHING)
#
# class ElderBrother(models.Model):
#     father_id = models.ForeignKey(Father,on_delete=models.DO_NOTHING)
#     younger_brother = models.ManyToManyField(YoungerBrother)
#
# class YoungerBrother(models.Model):
#     pass





# 增删改查基本操作

from juheapp.models import User
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'fivth_django.settings'
django.setup()

def ranstr(length):
    CHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    salt = ''
    for i in range(length):
        salt += random.choice(CHS)
    return salt

# 添加一个用户
def add_one():
    # 1
    user = User(open_id = 'test_open_id', nickname='test_nickname')
    user.save()

    # 2
    User.objects.create(open_id = 'test_open_id2', nickname='test_nickname2')

# 增：批量
def add_batch():
    new_user_list = []
    for i in range(10):
        open_id = ranstr(32)
        nickname = ranstr(10)
        user = User(open_id=open_id, nickname=nickname)
        new_user_list.append(user)
    User.objects.bulk_create(new_user_list)

# 查询
def get_one():
    user = User.objects.get(open_id='test_open_id')
    print(user)

# 数据过滤
def get_filter():
    users = User.objects.filter(open_id__contains='test_')
    # open_id__startswith
    # 大于: open_id__gt(greater than)
    # 小于: open_id__lt(little than)
    # 大于等于：open_id__gte(greater than equal)
    # 小于等于：open_id__lte(little than equal)
    print(users)

# 数据排序
def get_order():
    users = User.objects.order_by('open_id')
    print(users)

# 连锁查询
# 和管道符类似
def get_chain():
    users = User.objects.filter(open_id__contains='test_').order_by('open_id')
    print(users)

# 改一个
def modify_one():
    user = User.objects.get(open_id = 'test_open_id')
    user.nickname = 'modify_username'
    user.save()

# 批量改
def modify_batch():
    User.objects.filter(open_id__contains='test_').update(nickname='modify_uname')

def delete_one():
    User.objects.get(open_id='test_open_id').delete()

# 批量删除
def delete_batch():
    User.objects.filter(open_id__contains='test_').delete()

# 全部删除
def delete_all():
    User.objects.all().delete()
    # User.objects.delete()




#数据库函数和时间函数
# ---------数据库函数----------------
# 数据库函数
# 字符串拼接：Concat

from django.db.models import Value
from django.db.models.functions import Concat
# annotate创建对象的一个属性, Value,如果不是对象中原有属性
def concat_function():
    user = User.objects.filter(open_id='test_open_id').annotate(
        # open_id=(open_id), nickname=(nickname)
        screen_name = Concat(
            Value('open_id='),
            'open_id',
            Value(', '),
            Value('nickname='),
            'nickname')
        )[0]
    print('screen_name = ', user.screen_name)


# 字符串长度： Length
from django.db.models.functions import Length


def length_function():
    user = User.objects.filter(open_id='test_open_id').annotate(
        open_id_length = Length('open_id'))[0]

    print(user.open_id_length)


# 大小写函数
from django.db.models.functions import Upper, Lower


def case_function():
    user = User.objects.filter(open_id='test_open_id').annotate(
        upper_open_id=Upper('open_id'),
        lower_open_id=Lower('open_id')
    )[0]
    print('upper_open_id:', user.upper_open_id, ', lower_open_id:', user.lower_open_id)
    pass

# 日期处理函数
# Now()

from blog.models import Article
from django.db.models.functions import Now

def now_function():
    # 当前日期之前发布的所有应用
    acticles = Article.objects.filter(publish_date__lte=Now())
    for acticle in acticles:
        print(acticle)


# 时间截断函数
# Trunc
from django.db.models import Count
from django.db.models.functions import Trunc


def trunc_function():
    # 打印每一天发布的应用数量
    article_per_day = Article.objects.annotate(publish_day=Trunc('publish', 'day'))\
        .values('publish_day')\
        .annotate(publish_num=Count('article_id'))

    for article in article_per_day:
        print('date:', article['publish_day'], ', publish num:', article['publish_num'])

trunc_function()


