from django.views.generic.base import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'
    #템플릿뷰 상속시 필수적으로 템플릿 이름을 오버라이딩 해줘야 함(붙여줘야 함)
