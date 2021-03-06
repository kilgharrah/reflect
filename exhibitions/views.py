from django.views.generic import View, ListView, DetailView
from django.template.response import TemplateResponse, HttpResponse

from exhibitions.models import Exhibition
from utils.tools import getIntro

class ExhibitionList(ListView):
    context_object_name = "exhibition_list"
    template_name = "exhibition_list.html"
    paginate_by = 10

    def get_queryset(self):
        return Exhibition.objects.all().order_by('-from_date')

    def get_context_data(self, **kwargs):
        context = super(ExhibitionList, self).get_context_data(**kwargs)

        context['intro'] = getIntro(2)
        return context


class ExhibitionDetail(DetailView):
    model = Exhibition
    template_name = 'exhibition_detail.html'
    queryset = Exhibition.objects.all()

    def __init__(self, *args, **kwargs):
        super(ExhibitionDetail, self).__init__(*args, **kwargs)
        self.pictures = None
        self.intro = None

    def get_queryset(self):
        qs = super(ExhibitionDetail, self).get_queryset()
        slug = self.kwargs.get('slug', None)

        if slug:
            qs = qs.filter(slug=slug)

        return qs


    def get_context_data(self, **kwargs):
        context = super(ExhibitionDetail, self).get_context_data(**kwargs)

        self.pictures = self.object.picture_set.all()

        context['pictures'] = self.pictures
        context['intro'] = getIntro(2)

        return context
