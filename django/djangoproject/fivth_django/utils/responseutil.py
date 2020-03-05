class Code:
    SUCCESS = 2000
    FAILED = 2222
    @classmethod
    def des(cls,code):
        if code == cls.SUCCESS:
            return 'success'
        elif code == cls.FAILED:
            return 'failed'
        else:
            return "I don't know"


class ResponseMixin():
    @staticmethod
    def wrap_response(response):
        if not response.get('code'):
            response['code'] = Code.SUCCESS
        if not response.get('codedes'):
            response['codedes'] = Code.des(response.get('code'))
        return response