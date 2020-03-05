# import json,requests
# from utils import proxy
# import fivth_django.settings
# from juheapp.models import User
#
# from utils.wx.crypt import WXBizDataCrypt
# from utils.code2session import code2session
#
# #判断是否已经授权
# def already_authorized(request):
#     is_authorized = False
#     if request.session.get('is_authorized'):
#         is_authorized = True
#     return is_authorized
#
# def get_user(request):
#     if not already_authorized(request):
#         raise Exception('not authorized request')
#     open_id = request.session.get('open_id')
#     user = User.objects.get(open_id=open_id)
#     return user
#
#
# def c2s(appid,code):
#     return code2session(appid,code)
#
# def code2session(appid,code):
#     API = 'https://api.weixin.qq.com/sns/jscode2session'
#     # params = 'appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code'
#     params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % \
#              (appid, fivth_django.settings.WX_APP_SECRET, code)
#
#     url = API+'?'+params
#     response = requests.get(url=url,proxies=proxy.proxy())
#     data = json.loads(response.text)
#     print(data)
#     return data