from django.contrib import admin
from .models import Question

# Register your models here.

class QuestionAdmin(admin.ModelAdmin): # 세부 기능을 추가하기 위함
    search_fields = ['subject'] # admin 모델페이지 검색 속성

admin.site.register(Question, QuestionAdmin)