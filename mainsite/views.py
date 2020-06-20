from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
#테이블 레코드를 생성하기위해 필요한 폼을 보여주고 데이터를 입력받아 레코드 생성하는 제네릭뷰
from django.contrib.auth.forms import UserCreationForm
#User모델의 객체를 생성하기 위해 보여주는 폼이라고 함. 기본 제공
from django.urls import reverse_lazy
#reverse()함수를 쓰려면 url.py가 메모리에 로딩되어야 하는데, view처리 단계에서 로딩되지 않을수도
#있으므로 reverse_lazy함수를 썼다고 함

#개정판엔 있는 부분
from django.contrib.auth.mixins import AccessMixin
#mixin이란 상속하지 않고도 다른 클래스에서 사용가능한 클래스. 상속으로 인한 모호성문제를 방지하는 용도라고 함
from django.views.defaults import permission_denied

from django.contrib.auth.decorators import login_required
#login~함수는 데코레이터로 사용되는 함수로 일반 함수에 적용. 기능은 로그인시 원래함수를 실행하고,
#아닐시 로그인페이지로 리다이렉트

#Homepage
class HomeView(TemplateView):
    template_name = 'home.html'
    #템플릿뷰 상속시 필수적으로 템플릿 이름을 오버라이딩 해줘야 함(붙여줘야 함)

#User Creation
class UserCreateView(CreateView):
    #CreateView를 상속받는다는 이야기는 FormView가 기본적으로 상속받아진다는 이야기.
    template_name = 'registration/register.html'
    form_class = UserCreationForm #미리 정의된 폼을 보여준다고 함. 직접 개발도 가능
    #UserCreatoinForm에 정의된 form의 필드값들이 템플릿에서 호출됨
    success_url = reverse_lazy('register_done') #에러검사 후 없으면 테이블 생성후 이 url을 띄움
    #/account/register/done/

class UserCreateDoneTV(TemplateView): #/account/register/done/를 처리하는 view
    template_name = 'registration/register_done.html'#가입처리 완료후 보여줄 템플릿 파일명 지정

#글쓴이만 수정/삭제 할 수 있도록 만든 클래스. 파이참상에서는 함수를 찾을 수 없다 나오지만, 실제로 실행해보면
#정상적으로 동작. 아마도 실제 실행하는 과정에서 해당 함수들이 미리 호출되어 처리되는 듯.
class OwnerOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "Owner only can update/delete the object"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.owner:
            self.handle_no_permission()
        return super().get(request, *args, **kwargs)

# # Login~~클래스를 상속받는 클래스의 as_view()메소드를 호출하면, 다중상속 구조의 메소드를
# #호출하는 순서에 의해 view클래스의 as_view메소드에 login_required()가 적용됨(과거방식. 아예 새로 mixin제공)
# class LoginRequiredMixin(object): #login_required함수는 함수에만 적용가능. object기능 상속으로 처리
#     #따라서 클래스형 뷰에서는 이를 상속받아 사용하면 login_required데코레이터 기능을 쓸 수 있음
#     @classmethod
#     def as_view(cls, **initkwargs):#as_view메소드를 인스턴스메소드가 아닌 클래스 메소드로 정의
#         view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
#         #super메소드 정의에 의해 LoginR~~상위에 있는 as_view메소드가 view변수에 할당됨
#         return login_required(view)
#         #view변수 즉, LoginRe~~상위에 있는 as_view()메소드에 login_required()기능을 적용하고 이를 반환