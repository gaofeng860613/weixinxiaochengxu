一.Django的models.py数据库迁移(备份数据库, 创建新数据库, 把备份的数据导入到新数据库),迁移数据和表结构

1.数据备份

python manage.py dumpdata 应用名>xx.json

2.备份完成,会生成一个xx.json文件,此时在settings.py里配置DATABASES,把之前的改成:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    #slave不是固定的,可以任意起名
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        #数据库名是在数据库建好的
        'NAME': 'djangodatabase',
        'USER': 'root',
        'PASSWORD': 'xingpeixun',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }

}
```

运行命令:python manage.py migrate --run-syncdb --database slave

3.运行以上命令不报错,把上面DATABASES注掉,修改成:(也就是把slave改成default)

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangodatabase',
        'USER': 'root',
        'PASSWORD': 'xingpeixun',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

此时在运行命令 python manage.py loaddata xx.json,不报错证明数据库迁移成功,可打开数据库查看

二.数据库索引

- 应该被索引的字段
  1. 需要排序的字段(order_by)
  2. 需要比较操作的字段(> < >= <=)
  3. 需要过滤操作的字段(filter,exclude)

- 添加索引的两种方式

  1. 属性中定义

     - 对于模型字段添加db_index=True(查看索引用show index form 表名)
     - 任何表结构的改变都需要迁移数据库

  2. 模型的Meta属性类

     网址:

     1. https://docs.djangoproject.com/en/dev/ref/models/options/ 
     2. https://www.jianshu.com/p/774a8f16d624
     3. https://blog.csdn.net/bbwangj/article/details/79967858

- 默认的索引规则
  1. 主键必是索引
  2. 外键必是索引
  3. 唯一必是索引