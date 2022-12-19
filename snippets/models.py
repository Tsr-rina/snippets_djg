from django.db import models
from django.conf import settings


class Snippet(models.Model):
    title = models.CharField('タイトル', max_length=128)
    description = models.TextField('説明', blank=True)
    created_at = models.DateTimeField('投稿日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    # インナークラスMeta
    class Meta:
        # テーブル名を設定する
        db_table = "snippets"

    def __str__(self):
        return f'{self.pk} {self.title}'

class Comment(models.Model):
    text = models.TextField("本文", blank=False)
    # 一対多のフィールを作成する
    commented_to = models.ForeignKey(Snippet, verbose_name="スニペット", on_delete=models.CASCADE)

    class Meta:
        db_table = "comments"
    
    def __str__(self):
        return f'{self.pk} {self.title}'

class Tag(models.Model):
    name = models.CharField("タグ名", max_length=32)
    snippets = models.ManyToManyField(Snippet, related_name='tags', related_query_name='tag')

    class Meta:
        db_table = "tags"
    
    def __str__(self):
        return f'{self.pk} {self.name}'