from rest_framework import viewsets, views

from api.models import Division, Employee


class DivisionAPIView(views.APIView):
    def get(self, request):
        l = Division.objects.all()
        

class DivisionViewSet(viewsets.ViewSet):
    def get(self, request):
        


