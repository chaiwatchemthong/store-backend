from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer, UserSerializer

def tokens_for(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    ser = RegisterSerializer(data=request.data)
    if not ser.is_valid():
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    user = ser.save()
    return Response({
        **tokens_for(user),
        'user': UserSerializer(user).data,
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email    = request.data.get('email', '')
    password = request.data.get('password', '')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'detail': 'อีเมลหรือรหัสผ่านไม่ถูกต้อง'}, status=status.HTTP_401_UNAUTHORIZED)
    if not user.check_password(password):
        return Response({'detail': 'อีเมลหรือรหัสผ่านไม่ถูกต้อง'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({
        **tokens_for(user),
        'user': UserSerializer(user).data,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)
