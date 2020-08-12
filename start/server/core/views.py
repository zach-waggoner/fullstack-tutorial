from django.views.generic import TemplateView


class AppView(TemplateView):
    template_name = "core/app.html"
