from django import forms
from .models import Post, Comment



class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title',  'subcontent', 'content','image','author','featured')



class CommentForm(forms.ModelForm):

    content = forms.CharField(label='Comment',widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'content',
        'rows': '4',
    }))


    class Meta:
        model = Comment
        fields = ('content',)
