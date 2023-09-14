from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class MyAccountManager(BaseUserManager):
	def create_user(self, email,first_name,last_name,phone_number, password=None):
		if not email:
			raise ValueError('Users must have an email address')


		user = self.model(
			email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
			phone_number=phone_number,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email,first_name,last_name,phone_number,  password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
            first_name=first_name,
            last_name=last_name,
			phone_number=phone_number,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user




class User(AbstractBaseUser):
	image=models.ImageField(upload_to='Student/profile')
	first_name=models.CharField(max_length=50,default='')
	last_name=models.CharField(max_length=50,default='')
	phone_number=models.CharField(max_length=50,default='')
	email=models.EmailField(unique=True, max_length=225)
	cls_name=models.CharField(max_length=50,default='')
	password=models.CharField(max_length=258,default='')
	DOB=models.DateField(auto_now_add=False)
	CHOICES = (
	("student", "student"),
	("teacher", "teacher"),
	)
	usertype=models.CharField(max_length=50,choices=CHOICES, default='student')
	status=models.BooleanField(default=False)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['country_code','phone_number']

	objects = MyAccountManager()

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True


class User_token(models.Model):
	User=models.OneToOneField(User,on_delete=models.CASCADE,related_name='token')
	token=models.CharField(max_length=10,default='')
	def __str__(self):
		return 'ID='+str(self.id)+'user='+str(self.User)+'token='+str(self.token)