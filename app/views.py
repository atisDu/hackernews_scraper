from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from app.models import Post
from core.serializer import ReactSerializer
from app.services import scraper

#ViewSeti parasto view vietā, lai strādātu ērtāk ar Datatables
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = ReactSerializer
    
    @action(detail=False, methods=['post'])
    def scrape(self, request):
        
        start_page_nr = request.data.get('start_page', 1)
        end_page_nr = request.data.get('end_page', 10)
        
        #Palaiž scraper service scriptu un tā funkciju ar lapas nr.
        scraper.multi_page_scrape(int(start_page_nr), end_page_nr)
        scraper.multi_page_update(int(start_page_nr), end_page_nr)
        
        queryset = Post.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_scores(self, request):

        start_page_nr = request.data.get('page', 1)
        
        #Palaiž scraper service scriptu un tā funkciju ar lapas nr.
        end_page_nr = 10 + int(start_page_nr) - 1
        scraper.multi_page_update(int(start_page_nr), end_page_nr)
        queryset = Post.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



#Lai fetchotu visu db
class ReactView(APIView):
    serializer_class = ReactSerializer

    def get(self, request):
        queryset = Post.objects.all().order_by('-posted_at') # Kārto pēc jaunākajiem ierakstiem
        serializer = ReactSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

