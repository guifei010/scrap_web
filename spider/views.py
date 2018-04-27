from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import CreateView, ListView, DetailView, ArchiveIndexView
import requests
import io
import hashlib
from django.core.files.base import ContentFile

from spider.taobao_test import get_taobao
from .forms import KeywordForm, SearchForm
from .models import KeyWord, SearchTask, ItemData
# Create your views here.


class KeyWordCreateView(CreateView):
    model = KeyWord
    template_name = 'spider/keyword_create.html'
    form_class = KeywordForm


class KeyWordListView(ListView):
    model = KeyWord
    template_name = 'spider/keyword_list.html'


class KeyWordDetailView(DetailView):
    model = KeyWord
    template_name = 'spider/keyword_detail.html'


class SearchCreateView(CreateView):
    model = SearchTask
    template_name = 'spider/search_create.html'
    form_class = SearchForm

    def get_view_sale(self, view_sale):
        import re
        ret = re.findall(r'\d+', view_sale)
        if not ret:
            return 0
        return int(ret[0])

    def form_valid(self, form):
        # ret = super(SearchCreateView, self).form_valid(form)
        self.object = form.save()
        for i, item in enumerate(get_taobao("笔记本")):
            if i >= self.object.max_limit:
                break
            # print(item)
            url = "http:"+item['pic_url']
            image = requests.get(url).content

            item = ItemData(
                search_task=self.object,
                index=i,
                title=item['raw_title'],
                image=ContentFile(image, name=hashlib.md5(url.encode()).hexdigest()+'.jpg'),
                price=item['view_price'],
                location=item['item_loc'],
                seller=item['nick'],
                view_sales=self.get_view_sale(item['view_sales']),
            )
            item.save()
            # print(item)
        return redirect(self.get_success_url())


class SearchListView(ListView):
    model = SearchTask
    template_name = 'spider/search_list.html'


class SearchDetailView(DetailView):
    model = SearchTask
    template_name = 'spider/search_detail.html'


# class SearchIndexView(ArchiveIndexView):
#     # model = SearchTask
#     # template_name = 'spider/index.html'
def index(request):
    # return HttpResponse("展示！")
    return render(request, "index.html")