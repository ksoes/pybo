from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer


@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id) # get_object()는 pk로 쿼리셋을 필터링하고 queryset결과에서 object를 뽑아서 return시켜주는 함수
    if request.method == 'POST':
        form = AnswerForm(request.POST) # form에는 <tr>~</tr> 데이터가 들어간다.
        if form.is_valid():
            answer = form.save(commit=False) # answer에는 answer객체가 들어간다
            answer.author = request.user # author속성에 로그인계정 저장, request.user = 현재 로그인한 계정의 User모델 객체
            answer.create_date = timezone.now()
            answer.question = question
            answer.save() # db에 반영한다
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id)) # resolve_url은 실제 호출되는 URL 문자열을 리턴하는 장고의 함수

    else : # get방식일때
        form = AnswerForm()
    context = {'question':question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pybo 답변 수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author :
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            print('answer :', answer, 'type(answer) :', type(answer))
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer_id))

    else : # GET
        form = AnswerForm(instance=answer)
    context = {'answer':answer, 'form':form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id): # urls.py에서 <int:answer_id> 값!
    """
    pybo 답변 삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)
