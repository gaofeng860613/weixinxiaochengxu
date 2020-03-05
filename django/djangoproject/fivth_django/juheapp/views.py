from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse,FileResponse,JsonResponse
import requests

def hello_juhe(request):
    # url = 'http://apis.juhe.cn/ip/ipNew?ip=111.111.111.111&key=89b459c29d47c5f9f3de77ae80bcd21d'
    url = 'http://v.juhe.cn/joke/content/list.php?sort=desc&page=2&pagesize=5&time=1418816972&key=7641f4a34d4ac69073e22c227843f89f'
    res = requests.get(url)
    if res.status_code == 200:
        return HttpResponse(res.text)
    else:
        return HttpResponse('没有找到数据')


def testrequest(request):
    print('请求方法:',request.method)
    print('客户端信息:',request.META)
    print('get请求参数:',request.GET)
    print('请求头:',request.headers)
    print('cookies:',request.COOKIES)
    return HttpResponse('testrequest')


def image(request):
    f = open(r'static/对比.png', 'rb')
    # return HttpResponse(content=f.read(),content_type='image/png')
    return FileResponse(f, content_type='image/png')


def apps(request):
    # return JsonResponse(['微信','支付宝','QQ'],safe=False)
    import yaml
    filepath = r'D:\pycharm\djangoproject\fivth_django\fivth_django\appconfig.yaml'
    with open(filepath, 'r', encoding='utf8') as f:
        res = yaml.load(f, Loader=yaml.FullLoader)
    return JsonResponse(res, safe=True)


#回应图文内容
import os
from fivth_django import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'fivth_django.settings'


def image1(request):
    if request.method == 'GET':
        filepath = os.path.join(settings.STATIC_ROOT_SELF,'对比.png')
        # f = open(filepath,'rb')
        # return FileResponse(f,content_type='image/png')
        with open(filepath, 'rb') as f:
            return HttpResponse(f,content_type='image/png')
    elif request.method == 'POST':
        return HttpResponse('这是post请求')
    else:
        return HttpResponse(request.method+'还没实现')


#cbv方法
from django.views import View


class imageView(View):

    def get(self,request):
        filepath = os.path.join(settings.STATIC_ROOT_SELF, '对比.png')
        # f = open(filepath,'rb')
        # return FileResponse(f,content_type='image/png')
        with open(filepath, 'rb') as f:
            return HttpResponse(f, content_type='image/png')

    def post(self,request):
        return HttpResponse('这是post请求')


def wenben(request):
    if request.method == 'GET':
        return HttpResponse('我是测试文本GET')
    elif request.method == 'POST':
        return HttpResponse('我是测试文本POST')
    else:
        return HttpResponse('其它方法文本' + request.method)


#mixin多态继承
from utils.responseutil import ResponseMixin, Code


class test_mixin(View, ResponseMixin):

    def get(self, request):
        return JsonResponse(data=self.wrap_response({"url": "xxxxxx", "des": "I am fine", "code": 2000,
                                                     "codedes": "No problem"}))


#django 和 小程序图片的上传和下载
class loader_up_down_pic(View):

    def get(self,request):
        filepath = os.path.join(settings.STATIC_ROOT_SELF, '对比.png')
        with open(filepath, 'rb') as f:
            return HttpResponse(f, content_type='image/png')
        # return render(request,'juheapp/uploader_loader_pic.html')

    def post(self,request):
        # return HttpResponse('这是post请求')
        files = request.FILES
        print(type(files))
        def savepic(filename,content):
            with open(filename,'wb') as f:
                f.write(content)

        picdir = settings.STATIC_ROOT_SELF
        for key, value in files.items():
            filename = os.path.join(picdir, key[-8:])
            savepic(filename, value.read())
            print('key:',key[-8:])
            print('value:',value)

        return HttpResponse(filename)

    def delete(self, request):
        picdir = settings.STATIC_ROOT_SELF
        pic_name = request.GET.get('name')
        pic_full_name = os.path.join(picdir,pic_name)
        if os.path.exists(pic_full_name):
            os.remove(pic_full_name)
            return HttpResponse('图片删除成功')
        return HttpResponse('图片不存在')




#小程序模拟登陆
class CookieTest(View):

    def get(self,request):
        # print(dir(request))
        request.session['message'] = 'Test Django Session Ok'
        return JsonResponse({'key':'value'})



#负责接收cookie
class CookieTest2(View):

    def get(self,request):
        print(request.session['message'])
        print(request.session.items())
        return JsonResponse({'key2':'value2'})


# from utils.authorize import c2s
# class UserView(View):
#     def get(self,request):
#         return self.post(request)
#
#     def post(self,request):
#         print(request.GET)
#         return HttpResponse('authorize post ok.')
#
#
# def __authorize_by_code(request):
#     #使用wx.login得到的临时code到微信提供的code2session授权
#     post_data = request.body.decode('urf-8')
#     post_data = json.loads(post_data)
#     code = post_data.get('code').strip()
#     app_id = post_data.get('appId').strip()
#     nickname = post_data.get('nickname').strip()
#
#     response = {}
#     if not code or not app_id:
#         response['message'] = 'authorize failed, need entire authorization data.'
#         response['code'] = ReturnCode.BROKEN_AUTHORIZED_DATA
#         return JsonResponse(data=response,safe=False)
#     data = c2s(app_id,code)
#     openid = data.get('openid')
#     print('get openid:',openid)
#
#     if not openid:
#         response = ResponseMixin.wrap_response({'code':Code.FAILED,'codedes':'authorize failed'})
#         return JsonResponse(data=response,safe=False)
#     request.session['openid'] = openid
#     request.session['is_authorized'] = True
#     if not User.objects.filter(openid=openid):
#         new_user = User(openid=openid,nickname=nickname)
#         print('new_user:open_id:%s,nikename:%s'%(openid,nickname))
#         new_user.save()
#
#     response = ResponseMixin.wrap_response({'code':Code.SUCCESS,'codedes':'authorize success'})
#     return JsonResponse(data=response,safe=False)
#
# def authorize(request):
#     return __authorize_by_code(request)



from fivth_django.settings import WX_APP_SECRET,WX_APPID
import json
from juheapp.models import User
class UserView(View):
    def get(self,request):
        return self.post(request)

    def post(self,request):
        print('request.body:',request.body)
        bodystr = request.body.decode('utf-8')
        bodydict = json.loads(bodystr)
        code = bodydict.get('code')
        print('code:', code)
        nickname = bodydict.get('nickname')
        print('昵称:', nickname)

        #发起请求
        appid = WX_APPID
        secret = WX_APP_SECRET
        js_code = code
        API = 'https://api.weixin.qq.com/sns/jscode2session'
        params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % \
                     (appid, secret, js_code)
        url = API + '?' + params
        res = requests.get(url)
        print('res.text:',res.text)
        res_dict = json.loads(res.text)
        openid = res_dict.get('openid')

        if not openid:
            return HttpResponse('authorize fail')

        #给这个用户赋予状态
        request.session['openid'] = openid
        request.session['is_authorized'] = True

        #将用户保存到 数据库
        if not User.objects.filter(open_id=openid):
            new_user = User(open_id=openid, nickname=nickname)
            print('new_user:open_id:%s,nickname:%s'%(openid, nickname))
            new_user.save()

        return HttpResponse('authorize post ok.')



#完善个人资料
# def test_session(request):
#     request.session['message'] = 'Test Django Session OK!'
#     response = wrap_json_response(code=10000)
#     return JsonResponse(data=response, safe=False)


def code2session(appid, code):
    API = 'https://api.weixin.qq.com/sns/jscode2session'
    params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % \
             (WX_APPID, WX_APP_SECRET, code)
    url = API + '?' + params
    response = requests.get(url=url, proxies=proxy.proxy())
    data = json.loads(response.text)
    print(data)
    return data


def __authorize_by_code(request):
    '''
    使用wx.login的到的临时code到微信提供的code2session接口授权

    post_data = {
        'encryptedData': 'xxxx',
        'appId': 'xxx',
        'sessionKey': 'xxx',
        'iv': 'xxx'
    }
    '''
    response = {}
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    app_id = post_data.get('appId').strip()
    nickname = post_data.get('nickname').strip()
    code = post_data.get('code').strip()
    print(code)
    print(app_id)
    if not (app_id and code):
        response['result_code'] = 2500
        response['message'] = 'authorized failed. need entire authorization data.'
        return JsonResponse(response, safe=False)
    try:
        data = c2s(app_id, code)
    except Exception as e:
        print(e)
        response['result_code'] = 2500
        response['message'] = 'authorized failed.'
        return JsonResponse(response, safe=False)
    open_id = data.get('openid')
    if not open_id:
        response['result_code'] = 2500
        response['message'] = 'authorization error.'
        return JsonResponse(response, safe=False)
    request.session['open_id'] = open_id
    request.session['is_authorized'] = True

    print(open_id)
    # User.objects.get(open_id=open_id) # 不要用get，用get查询如果结果数量 !=1 就会抛异常
    # 如果用户不存在，则新建用户
    if not User.objects.filter(open_id=open_id):
        new_user = User(open_id=open_id, nickname=nickname)
        new_user.save()

    # message = 'user authorize successfully.'
    # response = wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
    return JsonResponse(response, safe=False)


def authorize(request):
    return __authorize_by_code(request)



#处理关注的数据
class focus_data(View):
    # 关注的城市、股票和星座
    def get(self, request):
        if not already_authorized(request):

            return JsonResponse({'key': '没登录认证'}, safe=False)
        open_id = request.session.get('openid')
        user = User.objects.get(open_id=open_id)
        data = {}
        data['focus'] = {}
        data['focus']['city'] = json.loads(user.focus_cities)
        data['focus']['stock'] = json.loads(user.focus_stocks)
        data['focus']['constellation'] = json.loads(user.focus_constellations)

        return JsonResponse(data=data, safe=False)
        pass

    def post(self, request):
        if not already_authorized(request):

            return JsonResponse(data='认证失败', safe=False)
        open_id = request.session.get('openid')
        user = User.objects.get(open_id=open_id)

        received_body = request.body.decode('utf-8')
        received_body = eval(received_body)

        cities = received_body.get('city')
        stocks = received_body.get('stock')
        constellations = received_body.get('constellation')

        #不是追加的形式,是覆盖原有记录
        #todo这个bug 可以自己修复下
        #前后端配合 更全面的逻辑,做更少的事,更健壮的事
        #前段每次加载界面时,获取数据,和新添加的数据混合,保存时都post到后台
        #后台只需要覆盖数据

        user.focus_cities = json.dumps(cities)
        user.focus_stocks = json.dumps(stocks)
        user.focus_constellations = json.dumps(constellations)
        user.save()


        return JsonResponse(data='修改成功', safe=False)


# 判断是否已经授权
def already_authorized(request):
    is_authorized = False

    if request.session.get('is_authorized'):
        is_authorized = True
    return is_authorized


def get_user(request):
    if not already_authorized(request):
        raise Exception('not authorized request')
    open_id = request.session.get('open_id')
    user = User.objects.get(open_id=open_id)
    return user


def c2s(appid, code):
    return code2session(appid, code)


#登出
class LogOut(View):
    def get(self,request):
        request.session.clear()
        return JsonResponse(data={'key':'logout'}, safe=False)


class UserStatus(View):
    def get(self,request):
        print('call get_status function...')
        if already_authorized(request):
            data = {"is_authorized":1}
        else:
            data = {"is_authorized":0}
        return JsonResponse(data, safe=False)


def weather(city):
    '''
    :param city: 城市名字
    :return: 返回实况天气
    '''
    key = 'dd63b7fcbee2a5768d6e190fe494143f'
    api = 'http://apis.juhe.cn/simpleWeather/query'
    params = 'city=%s&key=%s' % (city[:2], key)
    url = api + '?' + params
    print(url)
    response = requests.get(url=url)
    data = json.loads(response.text)
    print(data)
    result = data.get('result')
    realtime = result.get('realtime')
    response = {}
    response['temperature'] = realtime.get('temperature')
    response['direct'] = realtime.get('direct')
    response['power'] = realtime.get('power')
    response['humidity'] = realtime.get('humidity')
    # response = {}
    # response['temperature'] = 'temperature'
    # response['win'] = 'win'
    # response['humidity'] = 'humidity'
    return response


#天气
class Weather(View):
    def get(self, request):
        if not already_authorized(request):
            response = {'key':2500}
        else:
            data = []
            openid = request.session.get('openid')
            user = User.objects.filter(open_id=openid)[0]
            cities = json.loads(user.focus_cities)
            for city in cities:
                result = weather(city.get('city'))
                result['city_info'] = city
                data.append(result)
            response = data
        return JsonResponse(data=response, safe=False)
        pass

    def post(self, request):
        data = []
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        print(received_body)
        cities = received_body.get('cities')
        for city in cities:
            result = weather(city.get('city'))
            result['city_info'] = city
            data.append(result)
        response_data = {'key':'post..'}
        return JsonResponse(data=response_data, safe=False)