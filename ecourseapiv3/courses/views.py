from django.shortcuts import render
from rest_framework import viewsets, generics,status, parsers
from rest_framework.decorators import action #tao ra 1 api moi
from rest_framework.response import Response
from courses.models import *
from courses import serializers, paginators


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active = True)
    serializer_class = serializers.CourseSerializer
    pagination_class = paginators.Item_Paginations

# DUA VAO CAC TRUY VAN R DUA LEN DUONG DAN
    def get_queryset(self): # ghi de len phuong thuc get_query cua no
        queryset = self.queryset
        q = self.request.query_params.get('q') #q la param tren url
        if q:
            queryset = queryset.filter(name__icontains = q)

        cate_id = self.request.query_params.get('category_id') # category_id tuong tu nhu q
        if cate_id:
            queryset = queryset.filter(category_id = cate_id) # category_id la cua course,
                                                                # category__id: lay course join lai voi table category
        return queryset

    @action(methods=['get'], url_path='lesson', detail=True)#dinh nghia 1 api moi
    def get_lesson(self, request, pk):
        lesson  = self.get_object().lesson_set.filter(active = True) # lesson_set : xem set xem co the thay the bang related_name k?
        q = self.request.query_params.get('les') #les la param tren url
        if q:
            lesson = lesson.filter(subject__icontains=q)
        return Response(serializers.LessonSerializer(lesson, many=True).data, status=status.HTTP_200_OK) # many tra ra nhieu object
        # return Response()


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView): # RetrieveAPIView cho phep tim dua tren id
    queryset = Lesson.objects.prefetch_related('tags').filter(active = True)
    serializer_class = serializers.LessionDetailSerializer


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active = True)
    serializer_class =  serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser,] # tim hieu