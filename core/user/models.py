from django.db import models

import uuid
from core.abstract.models import AbstractManager, AbstractModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin 
from django.core.exceptions import ObjectDoesNotExist 
from django.http import Http404
# Create your models here.

class UserManager(BaseUserManager, AbstractManager):
    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404
        
    def create_user(self, username, email, password=None, **kwargs):
        """create and return a `User` with an email, phone, number, username and password"""
        if username is None:
            raise TypeError('Users must have a username')
        if email is None:
            raise TypeError('Users must have an email')
        if password is None:
            raise TypeError('Users must have an email')
        
        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, username, email, password, **kwargs):
        """create and return a `User` with superuser (admin) permissions"""
        if password is None:
            raise TypeError('superuser must have a password')
        if email is None:
            raise TypeError('Superusers must hava an email')
        if username is None:
            raise TypeError('Superusers must have a username')
        
        user = self.create_user(username,email,password, **kwargs)
        user.is_superuser = True
        user.is_staff = True 
        user.save(using=self._db)

        return user   


class User(AbstractModel, AbstractBaseUser,PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    bio = models.TextField(null=True)
    posts_liked = models.ManyToManyField('core_post.Post', related_name='liked_by')
    # avatar = models.ImageField(null=True, blank=True, upload_to=user_directory_path)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    def like(self,post):
        """Lie `post` if it hasnt been done yet"""
        return self.posts_liked.add(post)
    
    def remove_like(self, post):
        """Remove a like from a `post`"""
        return self.posts_liked.remove(post)
    
    def has_liked(self, post):
        """Return True if the user has liked a `post`"""
        return self.posts_liked.filter(pk=post.pk).exists()
    



