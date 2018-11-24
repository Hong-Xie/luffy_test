from django.utils.deprecation import MiddlewareMixin

class CorsMiddleWare(MiddlewareMixin):

    def process_response(self,request,response):

        if request.method=="OPTIONS":

            response["Access-Control-Allow-Headers"] = "Content-Type"

        response["Access-Control-Allow-Origin"] = "http://127.0.0.1:8080"

        return response