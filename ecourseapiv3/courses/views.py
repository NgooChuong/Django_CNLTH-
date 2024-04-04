from django.shortcuts import render
from rest_framework import viewsets, generics,status, parsers, permissions
from rest_framework.decorators import action #tao ra 1 api moi
from rest_framework.response import Response
from courses.models import *
from courses import serializers, paginators, perms



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

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        comments = self.get_object().comment_set.select_related('user').all()
        paginator = paginators.Item_Paginations()
        page  = paginator.paginate_queryset(comments,request)
        if page is not None:
            serializer = serializers.CommentSerializer(page, many= True)
            return paginator.get_paginated_response(serializer.data)
        return Response(serializers.CommentSerializer(comments, many=True).data,
                        status=status.HTTP_200_OK)
    def get_permissions(self):
        if self.action in ['create_comments','create_rating']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    # @action(methods=['post'], url_path='comments',detail=False)
    # def create_rating(self,request):
    #     rate = self.get_object().rating_set.create()

    @action(methods=['post'],url_path='like', detail=True) #tim hieu detail
    def create_like(self, request, pk):
        li, created = Like.objects.get_or_create(lesson=self.get_object(),
                                                 user=request.user)
        if not created:
            li.active = not li.active
            li.save()

        return Response(serializers.AuthenticatedLessonDetailsSerializer(self.get_object()).data)



    @action(methods=['post'], url_path='comments',detail=True)
    def create_comments(self, request, pk):
        user = request.user
        c = self.get_object().comment_set.create(content = request.data.get('content'),user = user)
        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView): #viewsets.ModelViewSet: lay tat ca api
    queryset = User.objects.filter(is_active = True)
    serializer_class =  serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser,] # tim hieu

    def get_permissions(self):
        if self.action in ['get_cur_user']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


    @action(methods=['get', 'patch'], url_path='cur-user',detail=False)
    def get_cur_user(self, request): #request.user: tra ve user dang dang nhap admin hien tai
        user = request.user
        if (request.method.__eq__('PATCH')):
            for k, v in request.data.items(): #request_data : du lieu can chinh sua
                setattr(user,k,v) # dong nghia user.k = v
            user.save()
        return Response(serializers.UserSerializer(user).data)

class CommentViewSet(viewsets.ViewSet,generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializers_class = serializers.CommentSerializer
    permission_classes = [perms.CommentOwner]