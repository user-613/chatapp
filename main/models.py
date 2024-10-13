from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    icon = models.ImageField(null=True, blank=True)


class Talk(models.Model):
    # メッセージ
    message = models.CharField(max_length=500)
    # 送信者
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_talk")
    # 受信者
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_talk"
    )
    # 時刻
    # auto_now_add=True とすると、そのフィールドの値には、オブジェクトが生成されたときの時刻が保存されます。
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} -> {}".format(self.sender, self.receiver)

class Message(models.Model):
    content = models.CharField("内容", max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_at = models.DateTimeField("投稿日時", auto_now_add=True)
    image = models.ImageField("画像", null=True, blank=True) # 追加
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_message")

    def __str__(self):
        return self.content