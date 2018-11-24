

class BaseResponse(object):

    def __init__(self):
        self.data=None
        self.error_msg=""
        self.code=1000

    @property
    def dict(self):

        return self.__dict__