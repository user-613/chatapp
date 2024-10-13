from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User, Talk


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class LoginForm(AuthenticationForm):
    pass


class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ("message",)


class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)
        labels = {"username": "新しいユーザー名"}
        help_texts = {"username": ""}


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
        labels = {"email": "新しいメールアドレス"}


class FriendsSearchForm(forms.Form):
    """友達の中からユーザーを検索"""

    keyword = forms.CharField(
        label="検索",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "ユーザー名で検索"}),
    )
class IconChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("icon",)
        labels = {"icon": "アイコン画像"}

class MessageForm(forms.ModelForm):
    tag = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
    )

    class Meta:
        model = Message
        fields = [
            "content",
            "image",  
        ]