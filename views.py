from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

# Create your views here.



class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)

        if not serializer.is_valid():
            return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})

        serializer.save()    

        user = User.objects.get(username = serializer.data['username'])
        token_obj , _ = Token.objects.get_or_create(user=user)

        return Response({'status': 200, 'payload': serializer.data, 'token': str(token_obj), 'message': 'You sent'})



from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class StudentAPI(APIView):

    # authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        Student_objs = Student.objects.all()
        serializer = StudentSerializer(Student_objs, many = True)
        print(request.user)
        return Response({'status': 200, 'payload': serializer.data})

    def post(self, request):
        serializer = StudentSerializer(data = request.data)
        
        if not serializer.is_valid():
            return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})

        serializer.save()    
        return Response({'status': 200, 'payload': serializer.data, 'message': 'You sent'})

    def patch(self, request):
        try:
            student_obj = Student.objects.get(id = request.data['id'])
            serializer = StudentSerializer(student_obj, data = request.data, partial = True)
            
            if not serializer.is_valid():
                return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})
            
            serializer.save()
            return Response({'status': 200, 'payload': serializer.data, 'message': 'You sent'})
        
        except Exception as e:
            return Response({'status': 403, 'message': 'Invalid id'})

    def delete(self, request):
        try:
            id = request.GET.get('id')
            student_obj = Student.objects.get(id = id)
            student_obj.delete()
            return Response({'status': 200, 'message': 'delete'})

        except Exception as e:
            return Response({'status': 403, 'message': 'invalid id'})











# @api_view(['GET'])
# def home(request):
#     Student_objs = Student.objects.all()
#     serializer = StudentSerializer(Student_objs, many = True)
#     return Response({'status': 200, 'payload': serializer.data})


# @api_view(['POST'])
# def post_student(request):
#     data = request.data
#     serializer = StudentSerializer(data = request.data)
    
#     if not serializer.is_valid():
#         return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})

#     serializer.save()    
#     return Response({'status': 200, 'payload': serializer.data, 'message': 'You sent'})


# @api_view(['PUT'])
# def update_student(request, id):
#     try:
#         student_obj = Student.objects.get(id = id)
#         serializer = StudentSerializer(student_obj, data = request.data, partial = True)
        
#         if not serializer.is_valid():
#             return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})
        
#         serializer.save()
#         return Response({'status': 200, 'payload': serializer.data, 'message': 'You sent'})
    
#     except Exception as e:
#         return Response({'status': 403, 'message': 'Invalid id'})
    

# @api_view(['DELETE'])
# def delete_student(request, id):
#     try:
#         student_obj = Student.objects.get(id = id)
#         student_obj.delete()
#         return Response({'status': 200, 'message': 'delete'})

#     except Exception as e:
#         return Response({'status': 403, 'message': 'invalid id'})
