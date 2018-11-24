

class PriceException(Exception):

    def __init__(self):
        self.msg="价格策略有问题，你不是人！"



class CommonException(Exception):
    def __init__(self,msg):
        self.msg =msg