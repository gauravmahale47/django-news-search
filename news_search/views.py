import json
from django.views import View
from newsapi import NewsApiClient
from django.core.paginator import Paginator
from news_search.models import SearchHistory
from django.shortcuts import render, redirect
from NewsSearchApp.settings import NEWS_API_KEY
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta


app_name = "news_search"


@method_decorator(login_required(login_url="auth_management:login"), name="dispatch")
class SearchNewsView(View):
    def get(self, request):
        """
        This method is used to render the search page.
        """

        return render(request, "news/search.html")


@method_decorator(login_required(login_url="auth_management:login"), name="dispatch")
class ResultView(View):
    def get(self, request):
        """
        This method is used to get the search results from the news api.
        """

        newsapi = NewsApiClient(api_key=NEWS_API_KEY)

        keyword = request.GET.get("keyword")
        new_data = False
        existing_flag = False

        if keyword:
            request.session["keyword"] = keyword
        else:
            keyword = request.session.get("keyword")


        try:
            # Check if the results are older than 15 minutes
            existing = SearchHistory.objects.get(keyword=keyword, user=request.user)
            existing_flag = True
            if datetime.now().timestamp() - existing.updated_at.timestamp() > 900:
                articles = newsapi.get_everything(
                    q=keyword, language="en", sort_by="publishedAt", from_param=str(existing.date + timedelta(days=1))
                )
                request.session[keyword] = articles
                new_data = True
            else:
                # If the results are not older than 15 minutes, fetch the results from the session
                articles = request.session[keyword]
        except:
            # If the results are not present in the database, fetch the results from the news api
            articles = newsapi.get_everything(
                q=keyword, language="en", sort_by="publishedAt"
            )
            request.session[keyword] = articles
            new_data = True

        # If the results are present in the database, update the results if they are older than 15 minutes
        if new_data:
            articles_dict = {"data": []}
            for article in articles["articles"]:
                articles_dict["data"].append(
                    {
                        "title": article["title"],
                        "url": article["url"],
                    }
                )

        # Paginate the articles
        paginator = Paginator(articles["articles"], per_page=9)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        if not existing_flag :
            SearchHistory.objects.create(keyword=keyword, user=request.user, results=json.dumps(articles_dict), date=articles["articles"][-1].get("publishedAt")[:10])
        elif new_data and existing_flag:
            existing.results = json.dumps(articles_dict)
            if articles.get("articles"):
                existing.date = articles["articles"][-1].get("publishedAt")[:10]
            existing.save()
        
        context = {"page_obj": page_obj, "keyword": keyword}
        return render(request, "news/results.html", context=context)


@method_decorator(login_required(login_url="auth_management:login"), name="dispatch")
class HistoryView(View):
    def get(self, request):
        """
        This method is used to get the search history of the user
        """

        history = SearchHistory.objects.filter(user=request.user).order_by("-updated_at")
        context = {"history": history}
        return render(request, "news/history.html", context=context)


@method_decorator(login_required(login_url="auth_management:login"), name="dispatch")
class HistoryDetailView(View):
    def get(self, request, keyword):
        """
        This method is used to get the search results of the user
        If the results are older than 15 minutes, it will fetch the results from the news api
        """

        try:
            existing = SearchHistory.objects.get(keyword=keyword, user=request.user)
            if datetime.now().timestamp() - existing.updated_at.timestamp() > 900:
                newsapi = NewsApiClient(api_key=NEWS_API_KEY)

                articles = newsapi.get_everything(
                    q=keyword, language="en", sort_by="publishedAt", from_param=str(existing.date + timedelta(days=1))
                )
                articles_dict = {"data": []}
                for article in articles["articles"]:
                    articles_dict["data"].append(
                        {
                            "title": article["title"],
                            "url": article["url"],
                        }
                    )

                existing.results = json.dumps(articles_dict)
                if articles.get("articles"):
                    existing.date = articles["articles"][-1].get("publishedAt")[:10]
                existing.save()
        except:
            pass
        return redirect("news_search:history")


sort_flag = False
@method_decorator(login_required(login_url="auth_management:login"), name="dispatch")
class SortByDateView(View):
    def get(self, request):
        """
        This method is used to sort the search results by date
        """
        global sort_flag
        sort_flag = not sort_flag

        keyword = request.session.get("keyword")
        articles = request.session[keyword]
        articles["articles"].sort(key=lambda x: x["publishedAt"], reverse=sort_flag)
        request.session[keyword] = articles

        # Paginate the articles
        paginator = Paginator(articles["articles"], per_page=9)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {"page_obj": page_obj, "keyword": keyword}
        return render(request, "news/results.html", context=context)