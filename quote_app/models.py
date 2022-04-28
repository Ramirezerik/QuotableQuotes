from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile ('^[_a-zA-Z0-9-]+(.[_a-zA-Z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})')


# Create your models here.
# USER MANAGER (VALIDATIONS)
class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        check = User.objects.filter(email =postData['email'])
        if len(postData['email']) < 1:
            errors['reg_email'] = "Must enter an email address!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['reg_email'] = "Email address not valid, enter valid email address!"
        elif check:
            errors['reg_email'] = "Email address has already been registered!"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        check = User.objects.filter(email =postData['login_email'])
        if not check:
            errors['login_email'] = "Email not registered!"
        else:
            if not bcrypt.checkpw(postData['login_password'].encode(), check[0].password.encode()):
                errors['login_email'] = "Email and password do not match!"
        return errors


# USERS MODEL 
class User(models.Model):
    # name = models.CharField(max_length= 25)    # wireframe does not call for name input in registration
    email = models.EmailField(max_length= 100)
    password = models.CharField(max_length= 25)
    # created_at = models.DataTimeField(auto_now_add=True)
    # updated_at = models.DataTimeField(auto_now=True)
    objects = UserManager()


# QUOTE MANAGER
class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['quoted_by']) < 2:
            errors['quoted_by'] = "Quoted by should be 2 or more characters."
        if len(postData['message']) < 10:
            errors['message'] = "Message should be 10 or more characters."
        return errors


# QUOTES MODEL
class Quote(models.Model):
    quoted_by = models.CharField(max_length=50)
    message = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="has_created_quotes", on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="favorited_quotes")
    # created_at = models.DataTimeField(auto_now_add=True)
    # updated_at = models.DataTimeField(auto_now=True)
    objects = QuoteManager()


