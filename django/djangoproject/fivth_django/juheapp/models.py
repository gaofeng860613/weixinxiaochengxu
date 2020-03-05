from django.db import models

# Create your models here.

class User(models.Model):
    #openid
    open_id = models.CharField(max_length=32, unique=True)
    #昵称
    nickname = models.CharField(max_length=256)
    #关注的城市
    focus_cities = models.TextField(default='[]')
    #关注的星座
    focus_constellations = models.TextField(default='[]')
    #关注的股票
    focus_stocks = models.TextField(default='[]')

    def __str__(self):
        return self.nickname

    # class Meta:
    #     '''
    #     元:描绘本身
    #     '''
    #     #把juheapp_user改成了abc
    #     db_table = 'abc'
    #     indexes = [
    #         models.Index(fields=['nickname'],name='indexnickname'),#都是数组
    #         # models.Index(fields=['first_name'],name='first_name_idx')
    #     ]