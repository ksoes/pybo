from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == 'POST': # data입력 후 버튼을 누르면 동일한 페이지가 post방식으로 요청딤
        form = QuestionForm(request.POST) # request.POST를 인수로 QuestionForm을 생성할 경우에는 request.POST에 담긴 subject, content 값이 QuestionForm의 subject, content 속성에 *자동으로 저장되어* 객체가 생성된다.
        if form.is_valid(): # form에는 <tr>~</tr> 값이 들어있다.
            question = form.save(commit=False) # models에 create_date가 있지만, form.py fields에 subject,content만 정의해서, 이상태에서 commit()하면 null오류가 난다(create_date는 값이 없기 떄문)
            question.author = request.user
            question.create_date = timezone.now() # 그래서 여기서 create_date값을 넣어준다.
            question.save() # quesion에는 subject의 값이 들어가있다.
            return redirect('pybo:index')
    else: # request.method == 'GET'
        form = QuestionForm()
    context = {'form':form}
    return render(request, 'pybo/question_form.html', {'form':form}) # {'form':form} -> 템플릿에서 질문 등록시 사용할 폼 엘리먼트를 생성할 때 쓰임.


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author :
        messages.error('수정권한이 없습니다!')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question) # instance를 기준으로 QuestionForm을 생성하지만 request.POST의 값으로 덮어쓰라는 의미
        if form.is_valid():
            question = form.save(commit=False) # ModelForm.save()는 ModelForm 인스턴스를 반환하지 않습니다. ModelForm에 의해 생성/업데이트된 모델의 인스턴스를 반환합니다.
            print('question :',question, 'type(question) :',type(question))
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else: # get방식일때
        form = QuestionForm(instance=question) # GET 요청인 경우 질문수정 화면에 조회된 질문의 제목과 내용이 반영될 수 있도록 다음과 같이 폼을 생성해야 한다.
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author :
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')