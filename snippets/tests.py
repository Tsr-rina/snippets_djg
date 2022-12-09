from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest
from snippets.views import top, snippet_new, snippet_edit, snippet_detail
from snippets.models import Snippet
from django.urls import resolve
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class TopPageRenderSnippetsTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username = "test_user",
            email = "test@example.com",
            password = "top_secret_pass001",
        )
        self.snippet = Snippet.objects.create(
            title = "title1",
            code = "print('hello')",
            description = "description1",
            created_by = self.user,
        )
    def test_should_return_snippet_title(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.snippet.title)
    def test_should_return_username(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.user.username)


# class TopPageTest(TestCase):
#     def test_top_returns_200_and_expected_title(self):
#         response = self.client.get("/")
#         self.assertContains(response, "Djangoスニペット", status_code=200)

#     def test_top_page_uses_expected_template(self):
#         response = self.client.get("/")
#         self.assertTemplateUsed(response, "snippets/top.html")      

# class TopPageViewTest(TestCase):
#     def test_top_returns_200(self):
#         request = HttpRequest()
#         response = top(request)
#         self.assertEqual(response.status_code, 200)
    
#     def test_top_returns_expected_content(self):
#         request = HttpRequest()
#         response = top(request)
#         self.assertEqual(response.content, b"Hello World")

# class CreateSnippetTest(TestCase):
#     def test_should_resolve_snippet_new(self):
#         found = resolve("/snippets/new")
#         self.assertEqual(snippet_new, found.func)

class SnippetDetailTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username = "test_user",
            email = "test@example.com",
            password = "secret",
        )
        self.snippet = Snippet.objects.create(
            title = "タイトル",
            code = "コード",
            description = "解説",
            created_by = self.user,
        )
    def test_should_use_expected_template(self):
        response = self.client.get("/snippets/%s/"% self.snippet.id)
        self.assertTemplateUsed(response, "snippets/snippet_detail.html")
    
    def test_top_page_returns_200_and_expected_heading(self):
        response = self.client.get("/snippets/%s/"% self.snippet.id)
        self.assertContains(response, self.snippet.title, status_code=200)    

    # def test_should_resolve_snippet_detail(self):
    #     found = resolve("/snippets/1/")
    #     self.assertEqual(snippet_detail, found.func)

class EditSnippetTest(TestCase):
    def test_should_resolve_snippet_edit(self):
        found = resolve("/snippets/1/edit/")
        self.assertEqual(snippet_edit, found.func)  
    