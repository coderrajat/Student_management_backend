from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from django.core.mail import send_mail
import random
import datetime
from django.db.models import Q
import secrets
import bcrypt
from django.core.serializers import serialize
from .tools import code, decode, codetoken, decodetoken, get_user, get_base64_to_img,create_coupon_code,beautify_errors



def login_required(*ag,**kg):
    def inner(func):
        def wrapper(*args,**kwargs):
            if 'HTTP_AUTHORIZATION'in args[1].META :
                try:
                    data=decodetoken(args[1].META['HTTP_AUTHORIZATION'])
                    time=datetime.datetime.strptime(data[2].split('.')[0],'%Y-%m-%d %H:%M:%S')
                except:
                    return Response({'success':'false','error_msg':'invalid token','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                if len(data)==4 and time>datetime.datetime.now():
                    uzr= get_user(*data)
                    if uzr!=[]:
                        if uzr.token.token=='':
                            return Response({'success':'false','error_msg':'USER NOT LOGGEDIN','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                        return func(*args,**kwargs)
                    else:
                        return Response({'success':'false','error_msg':'USER NOT LOGGEDIN','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                return Response({'success':'false','error_msg':'token expire','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'success':'false','error_msg':'no HTTP_AUTHORIZATION ','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
            return func(*args,**kwargs)
        return wrapper
    return inner


def login_student(userid,token=''):
    token=codetoken(userid,type='student',token=token)
    return token


def logout_provider(token):
    try:
        data=decodetoken(token)
        uzr=list(models.Providers.objects.filter(id=data[1]))

        if uzr!=[]:
            uzr=uzr[0]
            uzr.token.token=''
            uzr.token.save()
            return True
        else:
            return False
    except Exception as e:
        return False


class Student_Register(APIView):
    def get(self, request):
        f0=serializers.password()
        f1=serializers.Student_form()

        return Response({**f1.data,**f0.data
                            },status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        f1=serializers.Student_form(data=request.POST)
      
        if f1.is_valid():
            if models.User.objects.filter(phone_number=request.POST['phone_number']).exists():
                return Response({'success':'false',
                                        'error_msg':'This phone number already exists',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
            elif  models.User.objects.filter(email=request.POST['email']).exists():
                        return Response({'success':'false',
                                        'error_msg':'This email already exists',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
            
            try:
                uzr=models.User()
                uzr.first_name=request.POST['first_name']
                uzr.last_name=request.POST['last_name']
                uzr.phone_number=request.POST['phone_number']
                uzr.usertype='student'
                uzr.DOB=request.POST['DOB']
                uzr.email=request.POST['email']
                passw=serializers.password(request.POST['password'])
                if not passw.is_valid:
                    return Response({'success':'false',
                                        'error_msg':'',
                                        'errors':{**passw.data},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
                if request.POST['password']==request.POST['confirm_password']:
                    password=request.POST['password'].encode('utf-8')
                    uzr.password=bcrypt.hashpw(password,bcrypt.gensalt())
                    uzr.password=uzr.password.decode("utf-8")
                    uzr.save()
                    return Response({'success':'true',
                                        'error_msg':'',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({'success':'false',
                                        'error_msg':'This password is not matching',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'success':'false',
                                'error_msg':"Something Bad happened",
                                'errors':{},
                                'response':{str(e)},
                                },status=status.HTTP_400_BAD_REQUEST)


        else:
            return Response({'success':'false',
                                'error_msg':'this field is require',
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        



class Student_login_api(APIView):
    def get(self,request):
        f1=serializers.userlogin()
        return Response(f1.data,status=status.HTTP_202_ACCEPTED)
    def post(self,request):
        f1=serializers.userlogin(data=request.data)
        if (f1.is_valid()):
            user=list(models.User.objects.filter(email=request.POST['email']))
            print(user)
            if user!=[]:
                user=user[0]
            else:
                return Response({'success':'false',
                                    'error_msg':'email:user_not_exists',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)
            print(user)

            if user.status!=True:
                return Response({'success':'false',
                                    'error_msg':'Verified your mail',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)

            password=str(request.POST['password']).encode('utf-8')
            hash_pass=user.password.encode('utf-8')
            if bcrypt.checkpw(password,hash_pass):
                sec=''
                for i in range(10):
                    sec+=secrets.choice(secrets.choice([chr(ii) for ii in range(45,123)]))

                user.token.token=sec
                user.last_login=datetime.datetime.now()
                user.token.save()
                re=login_student(user.id,token=sec)
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{'user':serialize('json', [user])},
                                    'token':re,},status=status.HTTP_202_ACCEPTED)

            return Response({'success':'false',
                                'error_msg':'user_not_authenticated',
                                'response':{},
                                'errors':dict(f1.errors),

                                },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success':'false',
                                'error_msg':'log_in_parameters_not_correct',
                                'errors':dict(f1.errors),
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

class logout_provider_api(APIView):
    def get(self,request):
        val=logout_provider(request.META['HTTP_AUTHORIZATION'])
        if val:
            return Response({'success':'true',
            'error_msg':'',
            'response':{},},status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'success':'false',
                                'error_msg':'Logout fail',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
