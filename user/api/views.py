from django.shortcuts import get_object_or_404
from rest_framework import exceptions, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from user.api.mixins import SendEmailMixin
from user.models import User, WeekDayAvailable
from .serializers import (
    MyTokenObtainPairSerializer,
    UserAdminSerializer,
    UserLessInfoSerializer,
    UserSerializer,
    UserRegisterSerializer,
    UserLoginSerializers,
)
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView,
)
from .permissions import IsUserOrReadOnly, RequestUserOrAdminEdit
from mainproject.pagination import CustomPagination
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework_simplejwt.tokens import RefreshToken


# using custom tokenserializer to get userinfo in token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UsersList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class RegisterUserAPIView(APIView, SendEmailMixin):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    # email_template_name = "email/activation_email.html"
    # mail_subject  = "Activate Your Account "

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        roles = ["Freelancer", "Admin", "Employer"]
        if serializer.is_valid():
            username = serializer.data['username']
            username = serializer.data['email']
            password = serializer.data.get('password')

            role = serializer.data.get("role")
            if User.objects.filter(email=serializer.data["email"]).exists():
                raise exceptions.APIException("Email already taken !")
            if User.objects.filter(username=serializer.data["username"]).exists():
                raise exceptions.APIException(" Uername already taken !")
            if role not in roles:
                raise exceptions.APIException("Invalid Role !")
            # if not serializer.user.is_authenticated:
            #     if role == "Admin":
            #         raise exceptions.APIException("Invalid Role !")
            # else:
            #     if not request.user.role == "Admin":
            #         raise exceptions.APIException("Not enough permission !")
            user = User.objects.create_user(
                username=serializer.data.get("username"),
                email=serializer.data.get("email"),
                password=serializer.data["password"],
                role=role,
            )
            user.set_password(serializer.data['password'])
            user.is_active = True
            user.save()
            serializer = UserLessInfoSerializer(user, many=False)
            return Response(serializer.data)
        return Response(serializer.errors, 400)


# class RegisterUserApi(APIView,SendEmailMixin):
#     permission_classes = [AllowAny]
#     email_template_name = "email/activation_email.html"
#     mail_subject  = "Activate Your Account "

#     def post(self, request):
#         try:
#             data = request.data
#             roles = ["Freelancer", "Admin", "Employer"]
#             role = data.get("role")
#             if User.objects.filter(email=data["email"]).exists():
#                 raise exceptions.APIException("Email already taken !")
#             if User.objects.filter(username=data["username"]).exists():
#                 raise exceptions.APIException(" Uername already taken !")
#             if role not in roles:
#                 raise exceptions.APIException("Invalid Role !")
#             if not request.user.is_authenticated:
#                 if role == "Admin":
#                     raise exceptions.APIException("Invalid Role !")
#             else:
#                 if not request.user.role == "Admin":
#                     raise exceptions.APIException("Not enough permission !")

#             if data["password"] != data["password_confirm"]:
#                 raise exceptions.APIException( "Passwords do not match  !")

#             user =User.objects.create_user(
#                 username=data.get("username"),
#                 email=data.get("email"),
#                 password=data["password"],
#                 role=role,
#                 display_name=data['display_name']
#             )
#             user.set_password(data['password'])
#             user.is_active=False
#             user.save()
#             domain = request.META["HTTP_HOST"]
#             email_data = {
#                         "domain": domain,
#                         "uid": urlsafe_base64_encode(force_bytes(user.id)),
#                         "token": account_activation_token.make_token(user),
#                         "site_name": "Batuwa",
#             }
#             self.send_email_temp(email_data, user.email)
#             serializer = UserLessInfoSerializer(user,many=False)
#             return Response(serializer.data)
#         except Exception as e:
#             print('error is ',e)
#             return Response({"detail":str(e)})


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "username"
    lookup_field = "username"
    permission_classes = [RequestUserOrAdminEdit]

    def get_serializer_class(self):
        role = self.request.user.role
        if role == "Admin":
            return UserAdminSerializer
        else:
            return self.serializer_class


# password change by admin so old password is not necessary
class PasswordChangeAPIView(APIView):
    permission_classes = [RequestUserOrAdminEdit]

    def put(self, request, id):
        user = get_object_or_404(User, id=id)
        self.check_object_permissions(request, user)

        if len(request.data["new_password"]) < 6:
            raise exceptions.ValidationError(
                {"msg": "Passwords must be larger than 6 letters !"}
            )

        if request.data["new_password"] != request.data["password_confirm"]:
            raise exceptions.ValidationError(
                {"msg": "Passwords do not match  !"})

        user.set_password(request.data["new_password"])
        user.save()
        return Response({"msg": "Password Changed Succesfully"})


class PasswordResetApiView(APIView, SendEmailMixin):
    email_template_name = "email/password_reset_email.html"
    mail_subject = "Password Reset Requested"

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        print("email is ", email)
        if not email:
            return Response({"detail": "Email Required !", "sent": False})
        user = User.objects.filter(email=email).first()
        domain = request.META["HTTP_HOST"]
        if user:
            email_data = {
                "email": user.email,
                "domain": domain,
                "site_name": "Batuwa",
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": default_token_generator.make_token(user),
                "protocol": "http",
            }
            self.send_email_temp(email_data, email)
            return Response({"detail": "Sent Password Request Email", "sent": True})
        else:
            return Response(
                {"detail": "No User Found With This Email !", "sent": False}
            )


class SendActivationEmail(APIView, SendEmailMixin):

    permission_classes = [AllowAny]
    email_template_name = "email/activation_email.html"
    mail_subject = "Activate Your Account "

    def post(self, request):
        to_email = request.data.get("email")
        user = get_object_or_404(User, email=to_email)
        if user:
            if user.verified == False:
                domain = request.META["HTTP_HOST"]
                email_data = {
                    "domain": domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.id)),
                    "token": account_activation_token.make_token(user),
                    "site_name": "Batuwa",
                }
                self.send_email_temp(email_data, user.email)
                return Response({"detail": "Sent Verification Email"})
            else:
                return Response({"detail": "Already Verified Email !"})
        else:
            raise exceptions.APIException("User With This Email Not Found !!")


class WeekDayAvailableAPI(APIView, SendEmailMixin):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        import datetime
        data = request.data
        print(request.user)
        obj = get_object_or_404(WeekDayAvailable, id=data.get("id"))
        avail_from = data.get('available_from')
        avail_to = data.get('available_to')
        available_from = datetime.datetime.strptime(avail_from, '%H:%M').time()
        available_to = datetime.datetime.strptime(avail_to, '%H:%M').time()

        if available_from > available_to:
            return Response({"msg": "Available From cannot be greater than Available To !!"}, status=status.HTTP_400_BAD_REQUEST)
        obj.available_from = available_from
        obj.available_to = available_to
        obj.save()
        return Response({"msg": f"Updated time for {obj.name}."})


class UserLoginApiView(APIView):
    serializer_class = UserLoginSerializers
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = request.data['password']
            user = authenticate(username=email, password=password)
            if user:
                token = RefreshToken.for_user(user)
                data = UserLessInfoSerializer(user).data
                return Response({'refresh_token': str(token), 'access_token': str(token.access_token), 'user': data}, status=200)
            return Response({'message': "Invalid Credentials"}, status=401)
        return Response(serializer.errors, status=400)


class UserProfileViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "username"
    lookup_field = "username"
    permission_classes = [RequestUserOrAdminEdit]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)
