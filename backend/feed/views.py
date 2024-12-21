from django.shortcuts import render
import sys
import os
from django.http import HttpResponse
from authentication.views import logout_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import random
from faker import Faker
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Database.DatabaseCreation import DataBase
from django.http import JsonResponse
import json

#Create your views here.
fake = Faker()

DB = DataBase()

# Create your views here.
def posts(request):
    posts = DB.get_Posts()
    c = DB.get_Comments()
    users = DB.get_Users()
    user_id = request.session.get('user_id')
    user = DB.get_user(user_id)[0]
    print(user)
    return render(request, "../templates/Community/posts.html",{'users':users,'id':user_id,'user':user,'posts':posts,'comments':c}) #waiting for report to be passed here



def addPost(request):
    id = request.session.get('user_id')
    name = DB.get_userName(id)
    data = json.loads(request.body)
    description = data.get("description")
    photoUrl = data.get("photoURL")
    # name = data.get("posterName")

    update_response = DB.add_post(description,photoUrl,name )
    if update_response:
        return JsonResponse({'success': True })
    else:
        return JsonResponse({'success': False, 'error': 'cant update password'}, status=500)



def addComment(request):
    id = request.session.get('user_id')
    name = DB.get_userName(id)
    data = json.loads(request.body)
    description = data.get("comment")
    postID = data.get("postID")
    update_response = DB.add_comment_to_post(description,name,postID)
    if update_response:
                    
        return JsonResponse({'success': True })
    else:
        return JsonResponse({'success': False, 'error': 'cant update password'}, status=500)