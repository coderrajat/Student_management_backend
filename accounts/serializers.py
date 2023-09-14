from rest_framework import serializers
from . import models as account_models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed



def is_small(data):
    for i in data:
        if ord(i)>=97 and ord(i)<=122:
            return True
    return False

def is_large(data):
    for i in data:
        if ord(i)>=65  and ord(i)<=90:
            return True
    return False


def is_num(data):
    for i in data:
        if ord(i)>=48  and ord(i)<=57:
            return True
    return False


def is_special(data):
    for i in ['!','@','#','$','%','^','&','*']:
        if i in data:
            return True
    return False

def is_serise(data):
    a=0
    len=len(data)
    for i in range(data):
        if i==len-1:
            pass
        else:
            if ord(data[i])-ord(data[1+i]) in (-1,1):
                pass
            else:
                return True
    return False


def is_only_one_character(data):
    a=0
    len=len(data)
    for i in range(data):
        if i==len-1:
            pass
        else:
            if data[i]==data[1+i]:
                pass
            else:
                return True
    return False


def is_allowed(data):
    for i in data:
        if (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65  and ord(i)<=90) or (i in  ['!','@','#','$','%','^','&','*']) or (ord(i)>=48  and ord(i)<=57):
            print(i,ord(i))
            #pass
        else:
            print(i,ord(i),'error')
            return False
    return True


def validate(val):
    if len(val)<8:
        raise ValidationError(
            _('password must have at least 8 characters'),
            params={'val': val},
        )
    if not is_small(val):
        raise ValidationError(
            _('password must have at least 1 LowerCase Alphabet '),
            params={'val': val},
        )
    if not is_large(val):
        raise ValidationError(
            _('password must have at least 1 UpperCase Alphabet '),
            params={'val': val},
        )
    if not is_special(val):
        raise ValidationError(
            _('password must have at least 1 valid sepcial character  '),
            params={'val': val},
        )
    if not is_allowed(val):
        raise ValidationError(
            _('password must have only valid sepcial character  '),
            params={'val': val},
        )
    if not is_num(val):
        raise ValidationError(
            _('password must have at least 1 Numaric character'),
            params={'val': val},
        )
  
def is_all_number(val):
    for i in val:
        if ord(i)>57 or ord(i)<48:
            raise ValidationError(
                _('Phone Number should only contain numbers'),
                params={'val': val},
            )
        
class password(serializers.Serializer):
    password=serializers.CharField(required=False,validators=[validate])
    confirm_password=serializers.CharField(required=False)

class Student_form(serializers.Serializer):
    image=first_name=serializers.ImageField(required=False)
    first_name=serializers.CharField(required=False)
    last_name=serializers.CharField(required=False)
    DOB=serializers.CharField(required=False)
    phone_number=serializers.CharField(required=True,validators=[is_all_number])
    cls_name=serializers.CharField(required=False)
    email=serializers.CharField(required=True)


class userlogin(serializers.Serializer):
    email=serializers.CharField(max_length=200)
    password=serializers.CharField(max_length=155,required=False)