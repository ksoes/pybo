from django import forms
from pybo.models import Question, Answer, Comment

class QuestionForm(forms.ModelForm): # 모델 폼(ModelForm)을 상속
    class Meta:
        model = Question # 사용할 모델
        fields = ['subject', 'content'] # QuestionForm에서 사용할 Question모델의 속성
        # 즉, QuestionForm은 Question 모델과 연결된 폼이고 속성으로 Question 모델의 subject와 content를 사용한다고 정의한 것이다.
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }