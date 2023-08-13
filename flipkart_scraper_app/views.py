from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from .models import ScrappedData, JWTToken
from .serializers import ScrappedDataSerializer

class UserLogin(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = JWTToken.objects.get_or_create(user=user)
            return Response({'token': token.token})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

import requests
from bs4 import BeautifulSoup

class ScrapedDataAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        url = request.data.get('url')
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.find('span', {'class': 'B_NuCI'}).text.strip()
            price = soup.find('div', {'class': '_30jeq3 _16Jk6d'}).text.strip()
            description = soup.find('div', {'class': '_2o-xpa'}).text.strip() if soup.find('div', {'class': '_2o-xpa'}) else None
            num_reviews = int(soup.find('span', {'class': '_2_R_DZ'}).text.strip().split()[0])
            ratings = float(soup.find('div', {'class': '_2d4LTz'}).text.strip())
            media_count = len(soup.find_all('div', {'class': '_3T_wwx'}))
            
            scraped_data = {
                'url': url,
                'title': title,
                'price': price,
                'description': description,
                'num_reviews': num_reviews,
                'ratings': ratings,
                'media_count': media_count
            }
            
            scraped_data['user'] = request.user.id
            serializer = ScrappedDataSerializer(data=scraped_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Failed to scrape the URL'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
