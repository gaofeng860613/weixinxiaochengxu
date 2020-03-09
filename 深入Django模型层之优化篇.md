# 		一.深入Django模型层之优化篇

![](D:\projectgithub\weixinxiaochengxu\image\QQ截图20200308103645.png)

![](D:\projectgithub\weixinxiaochengxu\image\模型层.png)



# 二.Django末次那个层优化之理解模型变更与迁移

### 模型迁移的操作

![](D:\projectgithub\weixinxiaochengxu\image\QQ截图20200308104345.png)

makemigrations:讲模型层变更用Django的形式记录下来

migrate:执行模型变更,同步到数据库

### 迁移相关的命令

sqlmigtate:显示每次迁移执行的实际sql语句:python mange.py sqlmigrate 应用名 001(migrations里有很多自动生成的文件名)

showmigrations:显示某个应用的模型变更和迁移的历史: python manage.py showmigrations 应用名(迁移到数据库的文件前面会有一个[X],没有就是还没migrate)

### 迁移文件详解

migrations里很多自动生成的文件打开后里面会有dependencies和operations字段,自己可以看看,此文件可以自己写,但最好还是用pycharm IDE自动生成的

# 三.Django模型层优化之懒加载与预加载

### 懒加载的问题根源

- ORM的不透明

  ![](D:\projectgithub\weixinxiaochengxu\image\QQ截图20200308110212.png)

- 懒加载是什么

  1.存在于外键和多对多关系

  2.不检索关联对象的数据

  3.调用关联对象会再次查询数据库

- 查看Django ORM的数据加载

  ![](D:\projectgithub\weixinxiaochengxu\image\QQ截图20200308110659.png)

  menu是自定的:(会有一个 应用名_user_menu表)![](D:\projectgithub\weixinxiaochengxu\image\QQ截图20200308111251.png)

  users = User.objects.all()

  print(users.query)

  user = users[0]

  user_menu=user.menu.all()

  print(user_menu.query)

  查询两次对django和数据库,性能都是不好的,为了避免,可以预加载


### 预加载的方法

- 预加载单个关联对象---------select_related(选择相关)

- 预加载多个关联对象---------prefetch_related(预取相关)

- 相关操作:

  users= User.objects.prefetch_relatec('menu')

  第一次查询  用户表  第二次查询 APP表,再次查询直接从缓存里就可以查到

#### 预加载和懒加载性能对比(实际差多少与数据库模型定义样子和数据有关)

lazy_load.py

![](D:\projectgithub\weixinxiaochengxu\image\QQ截图20200308112654.png)

tools.py

```django
from db optimization. 6 lazy_ load import lazy_ load
class TimeTestTool:
	#计算函数这行的时间
	@classmethod
	def calc func time(cls, func):
		start = time perf counter()
		func()
		end = time . perf counter()
		return end-start
	#统计时间
	@classmethod
	def statistic_run_time(cls,func,n):
		data = [cls.calc_func_time(func) for i in range(n)]
		mean = statistics.mean(data)
		sd = statistics.stdev(data,xbar=mean)
		return [data,mean,sd,max(data),min(data)]
	#对比
	@classmethod
	def compare(cls,func1,func2,n):
		result1 = cls.statistic_run_time(fun1,n)
		result2 = cls.statistic_run_time(fun2,n)
		print('对比\t没有预加载\t预加载')
		print('平均值\t',result[1],'\t',result2[1])
if __name__ == '__main__':
TimeTestTool.compare(lazy_load.lazy_load,lazy_load.pre_load,100)
```

# 四.Django模型层优化之长连接

### 数据库链接的吃力逻辑

- 使用CONN_MAX_AGE配置限制DB链接寿命				(<https://docs.djangoproject.com/en/3.0/ref/settings/#conn-max-age>)
- CONN_MAX_AGE的默认值是0
- 每个DB链接的寿命保持到该次请求结束

### 链接方式

#### 短连接![](D:\projectgithub\weixinxiaochengxu\image\QQ截图20200309132641.png)

​	短连接的弊端:

​		1.每个请求都将重复链接数据库

​		2.处理高并发请求给服务器带来巨大压力

​		3.无法承受更高并发的服务

#### 长连接![](D:\projectgithub\weixinxiaochengxu\image\QQ截图20200309132845.png)

​	避免负优化:

​		1.存储数据库链接的位置:线程局部变量

​		2.数据库支持的最大链接

​			修改命令:查看最大链接数show variables like "%max_connection%";

​					修改最大链接数set global max_connections = number;

​		3.CONN_MAX_AGE的配置指南(部署线程数:n < 最大连接数:m;不建议使用)

​			![](D:\projectgithub\weixinxiaochengxu\image\QQ截图20200309134725.png)

短连接和长连接理论效果利用率:

​	![](D:\projectgithub\weixinxiaochengxu\image\QQ截图20200309135152.png)

# 五.数据库操作规范

### 使用正确的优化策略优化查询

- 正确使用索引(主键,唯一;作比较的,筛选的设成索引)

- 索引该被索引的列

  ​	1.如何使用索引

  ​	2.什么列该索引

- 不索引不应该被索引的列

### 使用iterator迭代器迭代QuerySet

- QuerySet非常大时,迭代器迭代节省内存
- len()错--->count()   (看多长)
- values   (看值)

### 理解对象的属性缓存

- 不可调用的属性会被ORM框架缓存(如User表里的nickname)
- 可调用的属性不会被ORM框架缓存(如menu,可以定一个变量menu=表类名.objects.all(),下次再用可直接使用变量,也可以起到优化作用)

### 数据库的公祖留给数据库做

- 过滤:使用filter,exclude等属性
- 聚合:使用annotate函数进行聚合
- 必要时,使用原本sql

### 正确检索行数据

- 使用被索引的列字段检索
- 使用被unique修饰额的列字段检索

### 不要进行不必要的检索

- QuerySet使用values(),value_list()函数返回python结构容器
- 查询结果长度使用QuerySet.count()而不是len(QuerySet)
- 判断是否为空使用QuerySet.exists()而不是if QuerySet
- 不要进行不必要的排序(男女生中先把男生筛选出来再排序这是可以的)

​	1.考虑数据足够小了吗

​	2.使用排序的列是索引吗

### 批量操作

- 大量数据的时候



原则:索引,QuerySet,能用orm框架提供的方法的就用orm框架的方法



### 附录

##### 参数mysqlx   max_connections:

- 其实这个属性从字面理解就可以理解是支持的最大链接数。不过这里多了"x"，那这怎么理解呢?MySQL是关系型数据库，在时代的车轮下，诸多新型数据库比如文档型数据库、kv数据库等等喷涌而现，MrS9L为应对时代变化，在5.7版本增加了插件'X Plugin", 用来支持提供类似文档数据库的服务。那么mysqlx max. connections指的就是这个插件最大能够支持的连接数了。