from django.shortcuts import render,get_object_or_404
from django.http import Http404,HttpResponseRedirect,JsonResponse,HttpResponse
from django.urls import reverse
from django import forms
from .forms import Get_Question,Get_Question_Auth,Get_Choices
from . import helpers

# Create your views here.
from .models import Question , Choice


#Get Quesitons
def index(request):
    if request.user.is_authenticated:
        latest_questions = Question.objects.order_by('-pub_date').filter(open_for_all=True)
    else:
        latest_questions = Question.objects.order_by('-pub_date').filter(open_for_all=True).filter(login_required=False)

        
    return render(request,"polls/index.html",{
        'latest_questions' : latest_questions
    })


#Get Details For A Poll
def votingPage(request,question_id):
    qid= helpers.hextoint(question_id)
    try:
        question = Question.objects.get(pk=int(qid))
        if question.login_required:
            if not request.user.is_authenticated:
                return render(request,'polls/notLoggedIn.html')
            else: 
                if len(question.voted_by.filter(pk=request.user.id))>0:
                    return render(request,'polls/alreadyVoted.html',{
                        'question':question
                    })

    except Question.DoesNotExist:
        raise Http404("Question Dies Not Exist")

    return render(request,"polls/votingPage.html",{
        'question':question
    })


#Get Results For A Poll
def results(request,question_id):
    qid= helpers.hextoint(question_id)
    question =  get_object_or_404(Question,pk=int(qid))
    return render(request,'polls/results.html',{
        'question':question
    })


#Vote For A Poll
def vote(request,question_id):
    qid= helpers.hextoint(question_id)
    question = get_object_or_404(Question,pk=qid)
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except(KeyError,Choice.DoesNotExist):
        return render(request,"polls/details.html",{
            'question':question,
            "error":"You Didn't Select A Choice",
        
        })
    else:
        if question.login_required:
            question.voted_by.add(request.user)
            
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question_id,)))


#Return A Chart
def resultsData(request,question_id):
    qid= helpers.hextoint(question_id)
    votes=[]
    question = Question.objects.get(pk=question_id)
    choices = question.choice_set.all()
    for i in choices:
        votes.append({
            i.choice_text:i.votes
        })
    return JsonResponse(votes,safe=False)


#Add A Poll
def addPoll(request):
    if request.method == 'POST':
        choices=[]
        if request.user.is_authenticated:
            q_form = Get_Question_Auth(request.POST,prefix='question')
        else:
            q_form = Get_Question(request.POST,prefix='question')
        c_form = Get_Choices(request.POST,prefix='choice')
        if(c_form.is_valid() and q_form.is_valid()):
            question = q_form.save()
            qid = question.link()
            # qid= helpers.hextoint(ques) 
            data = c_form.cleaned_data["choice"]
            choices =data.split(";")
            for choice in choices:
                ch = Choice(choice_text=choice,question=question)
                ch.save()

        return render(request,"polls/addPoll.html",{
            "q_form": q_form,
            "c_form": c_form,
            'submitted':True,
            "qid":qid
        })
    else:
        c_form = Get_Choices(prefix="choice")
        if request.user.is_authenticated:
            q_form = Get_Question_Auth(prefix='question')
        else:
            q_form = Get_Question(prefix='question')
        return render(request,"polls/addPoll.html",{
            "q_form": q_form,
            "c_form": c_form,
            'submitted':False,
        })