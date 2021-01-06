from .models import Question , Choice
from django import forms



##Model Form
class Get_Question(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text','open_for_all']
        widgets = {
          'question_text': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

class Get_Question_Auth(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text','open_for_all','login_required']
        widgets = {
          'question_text': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

class Get_Choices(forms.Form):
    choice = forms.CharField(label="Enter A Choice Seperated By ';' ",widget=forms.Textarea(attrs={'rows':2, 'cols':15}))
    
