# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

# Create your models here.

EMAIL_PATTERN = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class FriendManager(models.Manager):

    def validate_login(self, post_data):
        """
        check post request for valid data
        if valid returns tuple ([], <Friend Object>)
        if not returns ([error list], None)
        """
        errors = []


        # email exists in DB
        if not self.filter(email = post_data['email']):
            errors.append('Invalid email/password')

        else:
            # correct pw on user in DB
            user = self.get(email=post_data['email'])
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('Invalid email/password')
        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        """
        checks post request for valid data,
        if valid returns tuple ([], <Friend Object>)
        if not returns ([error list], None)
        """
        errors = []
        user = None
        # all fields are required
        for field, value in post_data.iteritems():
            if len(value) < 1:
                errors.append("All fields are required")
                break

        # min length on name fields (3)
        if len(post_data['name']) < 2 or len(post_data['alias']) < 2:
            errors.append("Name fields must be 2 or more")

        # min length on password
        if len(post_data['password']) < 8:
            errors.append("Password  must be 8 or more characters")

        # passwords match
        if post_data['password'] != post_data['password_confirm']:
            errors.append("password does not match")

        # email is a valid email
        if not re.match(EMAIL_PATTERN, post_data['email']):
            errors.append("invalid email")

        # email is in use
        if self.filter(email=post_data['email']):
            errors.append("email in use")



        # create user if no errors
        if not errors:
            hashed_pw = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt())

            user = self.create(
                name = post_data['name'],
                alias = post_data['alias'],
                email = post_data['email'],
                password = hashed_pw
            )
            return user
        return errors


class Friend(models.Model):

    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=250)
    # dob = models.DateField()

    objects = FriendManager()

    def __str__(self):
        return self.email

class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    poker = models.ForeignKey(Friend, related_name = "pokeamount")
    poking = models.ForeignKey(Friend, related_name = "poketake")
