from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from snippets.models import Snippet
from django.contrib.auth.decorators import login_required

from snippets.forms import SnippetForm


# Create your views here.

# render ->レスポンスを生成するためのメソッド
# createviewとか

def top(request):
    # Snippetの一覧を取得
    snippets = Snippet.objects.all()
    context = {"snippets":snippets}
    return render(request, "snippets/top.html", context)

@login_required
def snippet_new(request):
    if request.method == "POST":
        # SnippetFormのインスタンスを生成
        form = SnippetForm(request.POST)
        # 受け取ったパラメータがデータベースに登録して良いものかどうかを検証する
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.created_by = request.user
            snippet.save()
            return redirect(snippet_edit, snippet_id=snippet.pk)
    else:
        form = SnippetForm()
    return render(request, "snippets/snippet_new.html",{"form":form})

@login_required
def snippet_edit(request, snippet_id):
    # Snipppetからsnippet_idがあるかどうかを探してなかったら404を返す
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if snippet.created_by_id != request.user.id:
        return HttpResponse('このスニペットの編集の編集は許可されていません。')
    if request.method == "POST":
        form = SnippetForm(request.POST, instance=snippet)
        # is_valid()でバリデーションする
        if form.is_valid():
            form.save()
            return redirect("snippet_detail", snippet_id=snippet_id)
    else:
        form = SnippetForm(instance=snippet)
    return render(request, "snippets/snippet_edit.html", {"form": form})


def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    return render(request, "snippets/snippet_detail.html",{"snippet":snippet})