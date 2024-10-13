from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from .forms import (
    SignUpForm,
    LoginForm,
    TalkForm,
    UsernameChangeForm,  
    EmailChangeForm,
    FriendsSearchForm,
    IconChangeForm, 
)
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .models import User, Talk
from django.db.models import Q
from django.urls import reverse_lazy
from django.db.models import Max
from django.db.models.functions import Greatest, Coalesce
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView


def index(request):
    return render(request, "main/index.html")


def signup(request):
    if request.method == "GET":
        form = SignUpForm()
    elif request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            # モデルフォームは form の値を models にそのまま格納できる
            # save() メソッドがあるので便利
            form.save()

            # フォームから username と password を読み取る
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            # 認証情報のセットを検証するには authenticate() を利用します。
            # このメソッドは認証情報をキーワード引数として受け取ります。
            user = auth.authenticate(username=username, password=password)

            # 検証する対象はデフォルトでは username と password であり、
            # その組み合わせを個々の認証バックエンドに対して問い合わせ、
            # 認証バックエンドで認証情報が有効とされれば User オブジェクトを返します。
            # もしいずれの認証バックエンドでも認証情報が有効と判定されなければ
            # PermissionDenied エラーが送出され、None が返されます。
            # つまり、autenticate メソッドは"username"と"password"を受け取り、
            # その組み合わせが存在すればその User を返し、不正であれば None を返します。
            if user:
                # あるユーザーをログインさせる場合は、login() を利用します。
                # この関数は HttpRequest オブジェクトと User オブジェクトを受け取ります。
                # ここでの User は認証バックエンド属性を持ってる必要があり、
                # authenticate() が返す User は user.backend（認証バックエンド属性）を持つので連携可能。
                auth.login(request, user)

            return redirect("index")

    context = {"form": form}
    return render(request, "main/signup.html", context)


class LoginView(auth_views.LoginView):
    authentication_form = LoginForm  # ログイン用のフォームを指定
    template_name = "main/login.html"  # テンプレートを指定


class ForumView(ListView):
    template_name = "forum/forum.html"
    paginate_by = 5
    context_object_name = "friends"

    def get_queryset(self, **kwargs):
        queryset = (
            User.objects.exclude(id=self.request.user.id)
            .annotate(
                sent_talk__time__max=Max(
                    "sent_talk__time",
                    filter=Q(sent_talk__receiver=self.request.user),
                ),
                received_talk__time__max=Max(
                    "received_talk__time",
                    filter=Q(received_talk__sender=self.request.user),
                ),
                time_max=Greatest("sent_talk__time__max", "received_talk__time__max"),
                last_talk_time=Coalesce(
                    "time_max",
                    "sent_talk__time__max",
                    "received_talk__time__max",
                ),
            )
            .order_by("-last_talk_time")
            ("id", "username", "last_talk_time")
        )
        form = FriendsSearchForm(self.request.GET)
        if form.is_valid():
            keyword = form.cleaned_data["keyword"]
            if self.request.GET.get("tag"):
                queryset = queryset.filter(tag__name=self.requst.GET.get("tag"))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = FriendsSearchForm(self.request.GET)
        if form.is_valid():
            context["keyword"] = form.cleaned_data["keyword"]

        context["tag"] = self.request.GET.get("tag")
        return context


@login_required
def settings(request):
    return render(request, "main/settings.html")


@login_required
def talk_room(request, user_id):
    # get_object_or_404 は、第一引数にモデル名、その後任意の数のキーワードを受け取り、
    # もし合致するデータが存在するならそのデータを、存在しないなら 404 エラーを発生させます。
    friend = get_object_or_404(User, id=user_id)

    # 自分が送信者で上の friend が受信者であるデータ、または friend が送信者で friend が受信者であるデータをすべて取得します。
    talks = Talk.objects.filter(
        Q(sender=request.user, receiver=friend)
        | Q(sender=friend, receiver=request.user)
    ).order_by("time")

    if request.method == "GET":
        form = TalkForm()
    elif request.method == "POST":
        # 送信内容を取得
        form = TalkForm(request.POST)
        if form.is_valid():
            # トークを仮作成
            new_talk = form.save(commit=False)
            # 送信者、受信者、メッセージを与えて保存
            new_talk.sender = request.user
            new_talk.receiver = friend
            new_talk.save()
            return redirect("talk_room", user_id)

    context = {
        "form": form,  # 追加
        "friend": friend,
        "talks": talks,
    }
    return render(request, "main/talk_room.html", context)


@login_required
def username_change(request):
    if request.method == "GET":
        # instance を指定することで、指定したインスタンスのデータにアクセスできます
        form = UsernameChangeForm(instance=request.user)
    elif request.method == "POST":
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # 保存後、完了ページに遷移します
            return redirect("username_change_done")

    context = {"form": form}
    return render(request, "main/username_change.html", context)


@login_required
def username_change_done(request):
    return render(request, "main/username_change_done.html")


@login_required
def email_change(request):
    if request.method == "GET":
        form = EmailChangeForm(instance=request.user)
    elif request.method == "POST":
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("email_change_done")

    context = {"form": form}
    return render(request, "main/email_change.html", context)


@login_required
def email_change_done(request):
    return render(request, "main/email_change_done.html")

@login_required
def icon_change(request):
    if request.method == "GET":
        form = IconChangeForm(instance=request.user)
    elif request.method == "POST":
        form = IconChangeForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect("icon_change_done")

    context = {
        "form": form,
    }
    return render(request, "main/icon_change.html", context)

@login_required
def icon_change_done(request):
    return render(request, "main/icon_change_done.html")

class PasswordChangeView(auth_views.PasswordChangeView):
    """Django 組み込みパスワード変更ビュー

    template_name : 表示するテンプレート
    success_url : 処理が成功した時のリダイレクト先
    """

    template_name = "main/password_change.html"
    success_url = reverse_lazy("password_change_done")


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    """Django 標準パスワード変更ビュー"""

    template_name = "main/password_change_done.html"


class LogoutView(auth_views.LogoutView):
    pass

