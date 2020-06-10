from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
#테이블 레코드를 생성하기위해 필요한 폼을 보여주고 데이터를 입력받아 레코드 생성하는 제네릭뷰
from django.contrib.auth.forms import UserCreationForm
#User모델의 객체를 생성하기 위해 보여주는 폼이라고 함. 기본 제공
from django.urls import reverse_lazy
#reverse()함수를 쓰려면 url.py가 메모리에 로딩되어야 하는데, view처리 단계에서 로딩되지 않을수도
#있으므로 reverse_lazy함수를 썼다고 함

# #개정판엔 있는 부분
# from django.contrib.auth.mixins import AccessMixin
# #mixin이란 상속하지 않고도 다른 클래스에서 사용가능한 클래스. 상속으로 인한 모호성문제를 방지하는 용도라고 함
# from django.views.defaults import permission_denied

#Homepage
class HomeView(TemplateView):
    template_name = 'home.html'
    #템플릿뷰 상속시 필수적으로 템플릿 이름을 오버라이딩 해줘야 함(붙여줘야 함)

#User Creation
class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm #미리 정의된 폼을 보여준다고 함. 직접 개발도 가능
    success_url = reverse_lazy('register_done') #에러검사 후 없으면 테이블 생성후 이 url을 띄움
    #/account/register/done/

class UserCreateDoneTV(TemplateView): #/account/register/done/를 처리하는 view
    template_name = 'registration/register_done.html'#가입처리 완료후 보여줄 템플릿 파일명 지정

# 개정판에선 추가된 부분. 뭔가 상속부분에 에러가 있는 듯
# class OwnerOnlyMixin(AccessMixin):
#     raise_exception = True
#     permission_denied_message = "Owner only can update/delete the object"
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         if self.request.user != self.object.owner:
#             self.handle_no_permission()
#         return super().get(request, *args, **kwargs)

