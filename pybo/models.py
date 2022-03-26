from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question') # author 속성에 저장해야 하는 사용자 객체는 로그인 후 request 객체를 통해 얻을 수 있다.
    modify_date = models.DateTimeField(null=True, blank=True) # blank=True는 form.is_valid()를 통한 입력 데이터 검사 시 값이 없어도 된다는 의미이다.
    voter = models.ManyToManyField(User, related_name='voter_question') # 추천인 추가

    def __str__(self):
        return self.subject


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE) # 이 댓글이 달린 질문
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE) # 이 댓글이 달린 답변
    # 만약 질문댓글->question에 값 저장, 답변댓글->answer에 값 저장.
    # 댓글이 달렸을 때, answer와 question 동시에 값이 저장될 일이 없다!!!
