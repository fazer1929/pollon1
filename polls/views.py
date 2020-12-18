from django.shortcuts import render,get_object_or_404
from django.http import Http404,HttpResponseRedirect,JsonResponse,HttpResponse
from django.urls import reverse
from django import forms
from . import helpers

# Create your views here.
from .models import Question , Choice


##Model Form
class Get_Question(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text','open_for_all']
        widgets = {
          'question_text': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
     
class Get_Choices(forms.Form):
    choice = forms.CharField(label="Enter A Choice Seperated By ';' ",widget=forms.Textarea(attrs={'rows':2, 'cols':15}))
    

#Get Quesitons
def index(request):
    latest_question = Question.objects.order_by('-pub_date').filter(open_for_all=True)
    return render(request,"polls/index.html",{
        'latest_question' : latest_question
    })

#Get Details For A Poll
def details(request,question_id):
    qid= helpers.hextoint(question_id)
    try:
        question = Question.objects.get(pk=int(qid))
    except Question.DoesNotExist:
        raise Http404("Question Dies Not Exist")
    return render(request,"polls/details.html",{
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
        q_form = Get_Question(request.POST,prefix='question')
        c_form = Get_Choices(request.POST,prefix='choice')
        if(c_form.is_valid() and q_form.is_valid()):
            question = q_form.save()
            print(question)
            qid = question.link()
            # qid= helpers.hextoint(ques) 
            data = c_form.cleaned_data["choice"]
            choices =data.split(";")
            print(choices)
            for choice in choices:
                ch = Choice(choice_text=choice,question=question)
                ch.save()
            print(q_form.cleaned_data)

        return render(request,"polls/addPoll.html",{
            "q_form": q_form,
            "c_form": c_form,
            'submitted':True,
            "qid":qid
        })
    else:
        c_form = Get_Choices(prefix="choice")
        q_form = Get_Question(prefix='question')
        return render(request,"polls/addPoll.html",{
            "q_form": q_form,
            "c_form": c_form,
            'submitted':False,
        })