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
        
        page_nr = request.data.get('page', 1)
        
        #Palaiž scraper service scriptu un tā funkciju ar lapas nr.
        scraper.scrape(int(page_nr))
        scraper.update_score(int(page_nr))
        
        queryset = Post.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_scores(self, request):

        page_nr = request.data.get('page', 1)
        scraper.update_score(int(page_nr))
        queryset = Post.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




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

#Lai palaistu scrapera requestus atjaunot punktus un scrapot jaunus ierakstus
class ScrapeView(APIView):
    
    def post(self, request):
        try:
            #Dabon lapu nr. no requesta, noklusējumā = 1
            page_nr = request.data.get('page', 1)
            
            #Palaiž scraper service scriptu un tā funkciju ar lapas nr.
            scraper.scrape(int(page_nr))
            scraper.update_score(int(page_nr))
            
            #kārto pēc jaunākajiem ierakstiem !!lapā!!
            queryset = Post.objects.all().order_by('-posted_at')
            serializer = ReactSerializer(queryset, many=True)
            
            return Response({
                'status': 'success',
                'message': 'Scraped new post and updated scores.',
                'posts': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UpdateScoresView(APIView):
    #Lai atjaunotu punktus esošajiem ierakstiem automātiski refreshojot no fronta puses, bet citādi tas pats kas otrā
    
    def post(self, request):
        try:
            page_nr = request.data.get('page', 1)
            scraper.update_score(int(page_nr))
            
            queryset = Post.objects.all().order_by('-posted_at')
            serializer = ReactSerializer(queryset, many=True)
            
            return Response({
                'status': 'success',
                'message': 'Scores updated',
                'posts': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)