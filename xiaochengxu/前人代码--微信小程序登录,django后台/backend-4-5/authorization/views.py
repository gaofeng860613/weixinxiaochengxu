# -*- encoding=utf-8 -*-


import json

from django.http import JsonResponse
from django.views import View
from utils.response import wrap_json_response, ReturnCode, CommonResponseMixin
from utils.auth import already_authorized, c2s

from .models import User

def test_session(request):
    request.session['message'] = 'Test Django Session OK!'
    response = wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)


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
        response['result_code'] = ReturnCode.BROKEN_AUTHORIZED_DATA
        response['message'] = 'authorized failed. need entire authorization data.'
        return JsonResponse(response, safe=False)
    try:
        data = c2s(app_id, code)
    except Exception as e:
        print(e)
        response['result_code'] = ReturnCode.FAILED
        response['message'] = 'authorized failed.'
        return JsonResponse(response, safe=False)
    open_id = data.get('openid')
    if not open_id:
        response['result_code'] = ReturnCode.FAILED
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

    message = 'user authorize successfully.'
    response = wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
    return JsonResponse(response, safe=False)


def authorize(request):
    return __authorize_by_code(request)


class UserView(View, CommonResponseMixin):
    # 关注的城市、股票和星座
    def get(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.SUCCESS)
            return JsonResponse(data=response, safe=False)
        open_id = request.session.get('open_id')
        user = User.objects.get(open_id=open_id)
        data = {}
        data['focus'] = {}
        data['focus']['city'] = json.loads(user.focus_cities)
        data['focus']['stock'] = json.loads(user.focus_stocks)
        data['focus']['constellation'] = json.loads(user.focus_constellations)
        response = self.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)
        pass

    def post(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.SUCCESS)
            return JsonResponse(data=response, safe=False)
        open_id = request.session.get('open_id')
        user = User.objects.get(open_id=open_id)

        received_body = request.body.decode('utf-8')
        received_body = eval(received_body)

        cities = received_body.get('city')
        stocks = received_body.get('stock')
        constellations = received_body.get('constellation')

        user.focus_cities = json.dumps(cities)
        user.focus_stocks = json.dumps(stocks)
        user.focus_constellations = json.dumps(constellations)
        user.save()

        response = self.wrap_json_response(code=ReturnCode.SUCCESS, message='modify user info success.')
        return JsonResponse(data=response, safe=False)
        pass