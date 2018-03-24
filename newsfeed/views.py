from django.shortcuts import render, redirect
from .models import Article, Source
from .reddit_scraper import reddit_scraper
from .newsapi import techcrunch_scraper
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.debug import sensitive_variables, sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView, ListView, View
from django.utils import timezone
from .forms import *


def index(request):
    articles = Article.objects.order_by('-id')
    context = {
        'msg': "Hello Django World!",
               'articles': articles,
               }

    return render(request, 'index.html', context)


def news_list(request):
    subreddits = ['python', 'movies']  # temporarily fixed
    post_limit: int = 10
    articles = reddit_scraper(subreddits, post_limit)
    print(articles[10]['score'])
    articles += techcrunch_scraper()

    paginator = Paginator(articles, 10)
    page = request.GET.get('page', 1)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {'articles': articles}
    return render(request, 'news_list.html', context)


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    @method_decorator(sensitive_variables())
    @method_decorator(sensitive_post_parameters())
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['password_confirm']:
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            # returns user object if credentials they are OK
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(self.request, user)
                    return redirect('newsfeed:index')
            else:
                messages.error(self.request, "Invalid login or password")

        elif form.data['password'] != form.data['password_confirm']:
            form.add_error('password_confirm', 'The passwords do not match')

        return render(request, self.template_name, {'form': form})


def logout_view(request):
    logout(request)
    context = {}
    return render(request, 'logged_out.html', context)


class SourceDetailView(DetailView):

    model = Source
    template_name = 'detail_source.html'

    def get_context_data(self, **kwargs):
        context = super(SourceDetailView, self).get_context_data(**kwargs)
        source = self.object
        context['source_name'] = source.name
        context['url'] = source.url

        return context


class SourceListView(ListView):
    model = Source
    template_name = 'subscribe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
