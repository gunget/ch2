from django.shortcuts import render
from django.views.generic import ListView, DetailView
from photo.models import Album, Photo

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy #url.py가 로딩되기전에 reverse실행되는 것 방지.
from django.contrib.auth.mixins import LoginRequiredMixin #로그인 사용자만 생성할 수 있도록 하기
from mainsite.views import OwnerOnlyMixin #자기가 만든 것만 업데이트하고 지울 수 있게 하기

class AlbumLV(ListView):
    model = Album
    #template_name = 을 지정하지 않으면 default로 album_list.html이 됨
class AlbumDV(DetailView):
    model = Album
class PhotoDV(DetailView):
    model = Photo

class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['album', 'title', 'image', 'description']
    success_url = reverse_lazy('photo:index')

    #데코레이터처럼 부모클래스의 메소드를 호출하기 전에 내용을 추가하고 싶을때, 이런식으로
    # 같은 이름으로 재정의 하는 듯. 결론은 부모클래스의 같은 메소드를 호출하게 됨.
    def form_valid(self, form): #form_vaild의 재정의. owner항목에 user의 이름을 넣기 위해.
        form.instance.owner = self.request.user
        #form의 owner필드에 로그인된 user객체를 할당
        return super().form_valid(form)
    #제출된 form의 유효성 검사를 마친 후 이상이 없으면 form_valid메소드를 호출 함(CreateView의 자동 기능)

class PhotoChangeLV(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_change_list.html'

    def get_queryset(self):#현재 로그인된 사용자가 owner로 되어 있는 리스트만 뽑아내 리스트로 보여줌
        return Photo.objects.filter(owner=self.request.user)

class PhotoUpdateView(OwnerOnlyMixin, UpdateView):#실제로 바꾸기 할 뷰
    #지정된 레코드 하나를 폼으로 보여주고, 수정된 내용의 유효성 검사 후, 에러없으면 테이블에 추가
    model = Photo
    fields = ['album', 'title', 'image', 'description']
    success_url = reverse_lazy('bookmark:index')#수정 완료 후 이동할 url

class PhotoDeleteView(OwnerOnlyMixin, DeleteView):
    #기존 레코드 중에서 지정된 레코드를 삭제할 것인지 여부를 묻는 싸이트를 보여준다.
    model = Photo
    success_url = reverse_lazy('photo:index')

class AlbumChangeLV(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'photo/album_change_list.html'

    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user)

class AlbumDeleteView(OwnerOnlyMixin, DeleteView):
    model = Album
    success_url = reverse_lazy('album:index')

#인라인폼셋 처리를 위한 viwe코딩
from django.shortcuts import redirect #리다이렉트를 위한 숏컷 가져옴
from photo.forms import PhotoInlineFormSet #인스턴스 가져옴

class AlbumPhotoCV_revised(LoginRequiredMixin, CreateView):
    model = Album
    fields = ('name', 'description')
    success_url = reverse_lazy('photo:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PhotoInlineFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = PhotoInlineFormSet()
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        context = self.get_context_data()
        formset = context['formset']
        for photoform in formset:
            photoform.instance.owner = self.request.user
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


#폼셋이란 동일한 폼 여러개로 구성된 폼을 지칭. 또 인라인 폼셋이란 메인 폼에 딸려있는 하위 폼셋을 지칭
#테이블의 관계가 1:N일 경우, N테이블의 레코드 여러개를 동시에 입력받기 위한 용도로 인라인폼셋 사용.
class AlbumPhotoCV(LoginRequiredMixin, CreateView):
    #createView:중요한 몇가지 클래스속성만 정의해주면 적절한 폼을 보여주고 입력된 내용의 유효성 검사를 한뒤
    #이상이 없으면 입력된 내용으로 테이블에 레코드를 지정
    model = Album
    fields = ('name', 'description')
    success_url = reverse_lazy('photo:index')
    template_name = 'photo/album_form.html'

    #context의 확장을 위해 재정의
    def get_context_data(self, **kwargs): #context변수의 속성을 추가하기 위해 오버라이딩
        context = super().get_context_data(**kwargs)#부모것을 먼저 부른 뒤
        if self.request.POST:
            context['formset'] = PhotoInlineFormSet(self.request.POST, self.request.FILES)
            #formset이란 keyword에 request의 Post, FILE파라미터를 인라인 폼셋형태로 추가, context확장.
            #두 속성을 포함하여, 사진 폼셋을 앨범 context변수의 formset이란 속성에 인라인 폼셋형태로 지정한다.
            #하나의 앨범폼에 사진폼셋이 주르륵 붙어서 나타나도록 설정하기 위함인 듯

            '''
             템플릿에 넘겨줄 context(변수)에 추가적인 데이터를 넣고 싶을 경우, 이를 재지정 하면 된다.
             context는 기본적으로 딕셔너리이므로 딕셔너리 문법을 활용한다.
                def get_context_data(self, **kwargs):
                    # 기본 구현을 호출해 context를 가져온다.
                    context = super(PublisherDetail, self).get_context_data(**kwargs)
                    # 모든 책을 쿼리한 집합을 context 객체에 추가한다.
                    context['book_list'] = Book.objects.all()
                    return context
                처럼해서 추가적인 데이터를 넣을 수 있다(book_list항목을 넣어준 것) 
            '''
            ''' super().get_context_data(**kwargs)하면 호출되는 변수 값들. ListView를 상속받은 상태에서 불러온 예.
            {'paginator': None, 'page_obj': None, 'is_paginated': False, 'object_list': <QuerySet 
            [<Video: django 2.2>, <Video: django 1.11>]>, 'video_list': <QuerySet [<Video: django 2.2>, <Video: django 1.11>]>, 
            'view': <videos.views.VideoListView object at 0x106292cc0>}
            '''
            '''
            Django uses request and response objects to pass state through the system.
            When a page is requested, Django creates an [HttpRequest object] that contains
            metadata about the request. Then Django loads the appropriate view, passing
            the HttpRequest as the first argument to the view function. Each view is
            responsible for returning an [HttpResponse object].
             django.http모듈에 HttpRequest와 HttpResponse가 가지는 수십개의 API가 정의되어 있다.
            HttpRequest.FILE도 file업로드 정보를 딕셔너리 형태로 담은 HttpRequest객체의 속성이다.
             어떤 request용 api는 장고의 미들웨어가 추가하기도 하는데, 대보적인게 Request.user라는 api.
            이는 장고의 AuthentificationMiddleware가 추가한다.
            '''

            #보통 뷰는 return render(response, '.html', context)를 반환하는데, 이때 폼 뷰(edit view)의 경우
            #context = {'form':form}으로 보내진다. 여기서 form은 form객체. 헌데 여기선 인라인폼셋을 사용,
            #context ={'form':form, 'formset':PhotoIn~~}을 콘텍스트 변수로 템플릿에 반환하는 것으로 보인
            #다. 따라서 템플릿에선 form과 formset을 변수명으로 다 사용할 수 있다.
        else: #request가 post가 아니면 인라인 폼셋에 데이터가 들어가있지 않은 형태로 context 확장
            context['formset'] = PhotoInlineFormSet()
        return context

    #폼에 제출된 내용에 유효성 검사를 실행 후, 이상이 없으면 form_valid함수 실행
    #form은 앨범의 폼이고, formset은 form에 따라붙은 '사진 폼들'이라고 생각하고 접근해야 이해가 빠름
    def form_valid(self, form): #form은 CreateView가 만들어 표시했던 입력폼
        form.instance.owner = self.request.user #앨범의 owner필드에 사용자를 넣어라
        context = self.get_context_data() #context변수를 위에서 지정한 것처럼 확장
        formset = context['formset'] #그중 formset 부분만 추출해서 변수화(사진 폼만 처리하기 위해)
        for photoform in formset: #폼셋에 들어있는 사진 폼을 각각 호출
            photoform.instance.owner = self.request.user #사진 폼의 owner필드에 사용자 이름을 넣어라
        if formset.is_valid(): #사진폼들에 들어있는 각 데이터가 유효하다면,
            self.object = form.save() #앨범 폼의 데이터를 테이블에 저장. 곧 앨범 레코드를 하나 생성.
            formset.instance = self.object #저장한 앨범을(앨범객체) 폼셋의 메인객체로 지정.
            #곧 저장한 앨범에 '사진 폼 묶음'이 연계되도록 설정해준다.
            formset.save() #사진 폼의 데이터를 테이블에 저장. 곧, 사진 레코드를 여러개 생성.
            return redirect(self.object.get_absolute_url())#ex. photo/album/1/로 리디렉션
        else:
            return self.render_to_response(self.get_context_data(form=form))
            #사진 폼에 들어가있는 내용이 유효하지 않다면 다시 메인폼 및 폼셋을 다시 보여준다. 단, 이때
            #폼(앨범 폼)의 내용은 직전에 사용자가 입력한 내용을 다시 보여준다.

class AlbumPhotoUV(OwnerOnlyMixin, UpdateView):
    #UpdateView:중요한 몇가지 클래스속성만 정의해주면 지정된 레코드 하나의 내용을 폼으로 보여주고
    # 입력된 내용의 유효성 검사를 한뒤 이상이 없으면 입력된 내용으로 테이블에 레코드를 지정
    model = Album
    fields = ['name', 'description']
    template_name = 'photo/album_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PhotoInlineFormSet(self.request.POST, self.request.FILES,
                                                    instance=self.object)
            #create때와 차이라면 특정 앨범을 지정한 뒤 수정하는 것이므로, 현재 앨범 객체를 instance로 지정해
            #줘야 하는 듯.
        else:
            context['formset'] = PhotoInlineFormSet(instance=self.object)
            #get요청시 현재 앨범객체와 연결된 폼셋을 컨텍스트 변수로 추가
        return context

    def form_valid(self, form): #폼 유효성 검사후 자동 실행
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid: #사진 레코드가 유효하다면
            self.object = form.save() # 앨범 레코드를 수정
            formset.instance = self.object
            formset.save() #사진 레코드도 수정
            return redirect(self.object.get_absolute_url()) #ex. photo/album/1/로 리디렉션
        else:
            return self.render_to_response(self.get_context_data(form=form))
            #유효하지 않으면 폼과 인라인 폼셋을 다시 보여줌. 이때 내용은 전에 입력한 것 보여줌

# Create your views here.
