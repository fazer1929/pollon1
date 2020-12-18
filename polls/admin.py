from django.contrib import admin
from .models import Question,Choice
# Register your models here.

admin.site.site_header = 'Pollon Admin'
admin.site.site_title = 'Pollon Admin'
admin.site.index_title = 'Welcome To Pollon Admin'



class ChoiceInline(admin.TabularInline):
    model = Choice
    extra =2

class QuestionAdmin(admin.ModelAdmin):
    fieldsets=[(None,{'fields':['question_text']}),
    ('Date Information', {'fields':['pub_date'],'classes':['collapse']}),
    ('Open For All', {'fields':['open_for_all']}),
    ]
    inlines=[ChoiceInline]
    
admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)