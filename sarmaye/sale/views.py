from django.shortcuts import render
from .models import  Calculation
from asset.models import Asset
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from .serializers import CalculationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .serializers import CalculationRequestSerializer, CalculationResponseSerializer, MaxProfitResponseSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView



@csrf_exempt
def calculate_for_given_months(request):
    if request.method == 'POST':
        try:
            
            data = json.loads(request.body)
            user_id = data["user_id"]
            user = User.objects.get(id=user_id)
            first_month = data['first_month']
            last_month = data['last_month']
            given_money = int(data['given_money'])
            assets = Asset.objects.all()
            return_list = []
            for asset in assets:
                price1 = getattr(asset, first_month)
                price2 = getattr(asset, last_month)
                amount = given_money / price1
                finished_money = amount * price2
                profit = finished_money - given_money
                percentage = (profit / given_money) * 100
                Calculation.objects.create(user=user, asset=asset, start_month=first_month, end_month=last_month, given_money=given_money, profit=profit, percentage=percentage)
                return_list.append({'asset': asset.name, 'profit': profit, 'percentage': percentage})
            max_profit = {'max profit asset': None, 'profit': 0}
            for item in return_list:
                if item['profit'] > max_profit['profit']:
                    max_profit['max profit asset'] = item['asset']
                    max_profit['profit'] = item['profit']
            return_list.append(max_profit)
            return JsonResponse(return_list, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, safe=False)
@csrf_exempt
def calculate_for_given_asset(request, asset_name, user_id):
    try:
        user = User.objects.get(id=user_id)
        asset = Asset.objects.get(name = asset_name)
        attributes = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        max_profit = {'first_month': None, 'last_month': None, 'percentage': 0}
        for i in range(12):
            for j in range(i, 12):
                price1 = getattr(asset, attributes[i])
                price2 = getattr(asset, attributes[j])
                profit = (price2 - price1) / price1
                if profit > max_profit['percentage']:
                    max_profit['first_month'] = attributes[i]
                    max_profit['last_month'] = attributes[j]
                    max_profit['percentage'] = profit
        calculation = Calculation.objects.create(user = user, asset = asset, start_month = max_profit['first_month'], end_month = max_profit['last_month'], given_money = 0, profit = 0, percentage = max_profit['percentage'])
        return JsonResponse(max_profit, safe=False)
    except Asset.DoesNotExist:
        return JsonResponse({'error': 'Asset not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

class CalculationList(ListAPIView):
    serializer_class = CalculationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Calculation.objects.filter(user=user)

class CalculateForGivenMonthsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CalculationRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = request.user
                first_month = serializer.validated_data['first_month']
                last_month = serializer.validated_data['last_month']
                given_money = serializer.validated_data['given_money']
                
                assets = Asset.objects.all()
                return_list = []

                for asset in assets:
                    price1 = getattr(asset, first_month)
                    price2 = getattr(asset, last_month)
                    amount = given_money / price1
                    finished_money = amount * price2
                    profit = finished_money - given_money
                    percentage = (profit / given_money) * 100

                    Calculation.objects.create(
                        user=user,
                        asset=asset,
                        start_month=first_month,
                        end_month=last_month,
                        given_money=given_money,
                        profit=profit,
                        percentage=percentage
                    )

                    return_list.append({
                        'asset': asset.name,
                        'profit': profit,
                        'percentage': percentage
                    })

                max_profit = {'asset': None, 'profit': 0}
                for item in return_list:
                    if item['profit'] > max_profit['profit']:
                        max_profit['asset'] = item['asset']
                        max_profit['profit'] = item['profit']
                
                return_list.append(max_profit)
                
                response_serializer = CalculationResponseSerializer(return_list, many=True)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CalculateForGivenAssetView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, asset_name, user_id):
        try:
            user = User.objects.get(id=user_id)
            asset = Asset.objects.get(name=asset_name)
            attributes = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
            max_profit = {'first_month': None, 'last_month': None, 'percentage': 0}
            
            for i in range(12):
                for j in range(i, 12):
                    price1 = getattr(asset, attributes[i])
                    price2 = getattr(asset, attributes[j])
                    profit = (price2 - price1) / price1
                    if profit > max_profit['percentage']:
                        max_profit['first_month'] = attributes[i]
                        max_profit['last_month'] = attributes[j]
                        max_profit['percentage'] = profit
            
            # Optionally, create a calculation record
            Calculation.objects.create(
                user=user,
                asset=asset,
                start_month=max_profit['first_month'],
                end_month=max_profit['last_month'],
                given_money=0,
                profit=0,
                percentage=max_profit['percentage']
            )
            
            serializer = MaxProfitResponseSerializer(max_profit)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Asset.DoesNotExist:
            return Response({'error': 'Asset not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
            


