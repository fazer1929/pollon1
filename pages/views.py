from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from polls.models import Question
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    return render(request,'pages/index.html')


#See User Profile
def profile(request):
    if request.user.is_authenticated:
        questions = request.user.question_created.all().order_by('-pub_date')
        print(questions)
        return render(request,'pages/profile.html',{
            "questions":questions
        })
    else:
        return HttpResponseRedirect("/accounts/login")