from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from django.db.models import Sum

from user.serializers import AccountSerializer
from user.models import User, TotalScore
from user.serializers import TotalScoreSerializer
from bossRaid.models import BossRaidHistory
from bossRaid.serializers import BossRaidHistorySerializer

@csrf_exempt
def account_list(request):
    if request.method == 'GET':
        query_set = User.objects.all()
        serializer = AccountSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        account_db = User.objects.all()
        data = JSONParser().parse(request)
        if account_db.filter(username=data['username']).exists():
            return JsonResponse({'message':'ID is already exists!'}, status = 400)
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
@csrf_exempt
def account(request, pk):
    obj = User.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = AccountSerializer(obj)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AccountSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        obj.delete()
        return JsonResponse(status=204)
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user_id = data['username']
        obj = User.objects.get(username = user_id)
        
        if data['password'] == obj.password:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
    else:
        return JsonResponse({'message':'This method is not allowed.'}, status=400)


class TotalScoreAPI(mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """
    토탈 스토어 조회
    """

    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return TotalScoreSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs['user_id']
        history = BossRaidHistory.objects.filter(user_id=pk).all()
        boss_history = BossRaidHistorySerializer(history, many=True)

        # 사용자 상세 조회 시 총합 점수 및 히스토리 반환
        user = TotalScore.objects.get(user_id=pk)
        sum = BossRaidHistory.objects.aggregate(Sum('score'))['score__sum']
        user.total_score = sum
        user.save()

        res = {
            'totalScore': sum,
            'bossRaidHistory': boss_history.data
        }

        return Response(res, status=status.HTTP_200_OK)

