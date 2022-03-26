from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Question


def index(request):
    """
    pybo 목록 출력
    """
    # 입력  파라미터
    # http://localhost:8000/pybo/?page=1 처럼 get방식으로 호출된 URL에서 page값을 가져온다. pybo/라면 디폴트로 1.
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬 기준

    # 정렬
    # Question의 기존속성에 num_voter라는 속성을 하나 더 추가한다고 생각하면 쉽다.
    # 장고의 쿼리식 annotate : annotate로 num_voter를 지정하면 filter나 order_by에서 num_voter를 사용할 수 있게 된다.
    if so == 'recommend':  # 추천순
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':  # 답변 개수순
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')


    # 조회 - objects는 장고에서 자동을 추가하는 Manager객체이다.이걸로 필터링, 정렬 기타 여러 기능들을 할 수 있음.
    # question_list = Question.objects.order_by('-create_date')

    if kw:
        # *__icontains=kw : *에 kw문자열이 포함되어있는지를 의미
        question_list = question_list.filter(
            #  filter 함수에서 모델 속성에 접근하기 위해서는 이처럼 __ (언더바 두개) 를 이용하여 하위 속성에 접근함
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(author__username__icontains=kw) |  # 질문-글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변-글쓴이 검색
        ).distinct()

    # 페이징 처리
    # 인수 : 게시물 전체를 의미함 / 한 페이지당 10개. question_list를 가지고 paginator 객체 생성
    paginator = Paginator(question_list, 10)

    # get_page 메소드는 페이지 번호를 받아 해당 페이지를 리턴하게 됩니다
    # paginator를 이용하여 요청된 페이지(page)에 해당하는 페이징 객체(page_obj)를 생성 - page_obj에는 여러개의 속성들이 있음. ex). paginator.count, paginator.per_page
    page_obj = paginator.get_page(page)

    # question_list라는 키로 html에서 for문으로 값을 꺼낸다
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)  # django모델을 1번째 인자로 받음
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
