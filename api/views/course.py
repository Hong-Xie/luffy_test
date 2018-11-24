
from django.shortcuts import render ,HttpResponse

# Create your views here.

from rest_framework.views import  APIView
import json
from api.models import *

from api.serializers import CourseMiodelSerializers,CourseDetailMiodelSerializers
from rest_framework.response import Response

class coursesView(APIView):


    def get(self ,request ,*arg ,**kwargs):
        course_list=Course. objects.all()
        cs =CourseMiodelSerializers(course_list,many=True)
        print(cs.data)

        return Response(cs.data)

class CourseDetailView(APIView):


    def get(self ,request,pk,*arg ,**kwargs):
        coursedetail_obj=CourseDetail.objects.filter(pk=pk).first()
        cds =CourseDetailMiodelSerializers(coursedetail_obj)

        return Response(cds.data)