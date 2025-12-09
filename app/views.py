from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Post
from core.serializer import ReactSerializer

class ReactView(APIView):
    serializer_class = ReactSerializer

    def get(self, request):
        queryset = Post.objects.all()
        serializer = ReactSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)