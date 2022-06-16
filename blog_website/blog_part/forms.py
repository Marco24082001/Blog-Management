from unicodedata import category
from django import forms

from user_profile.models import User

from .models import Blog, Category

from ckeditor.fields import RichTextField

# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent

# import pandas as pd
# try:
#     # if Category.objects.filter(title = 'Thế Giới').exists():
#     # if Category.objects.filter(title = 'Pháp Luật').exists():
#     if Category.objects.filter(title = 'Giáo Dục').exists():
#         pass
#     else:
#         # cate = Category(title = 'Thế Giới')
#         # cate = Category(title = 'Pháp Luật')
#         cate = Category(title = 'Giáo Dục')
#         cate.save()
        
        
#     # df = pd.read_csv(BASE_DIR / 'TheGioi.csv')
#     df = pd.read_csv(BASE_DIR / 'GiaoDuc.csv')
#     for i in range(len(df)):
#         temp = Blog()
#         temp.user = User.objects.get(username = 'baotintuc')
#         # temp.category = Category.objects.get(title = 'Thế Giới')
#         temp.category = Category.objects.get(title = 'Giáo Dục')
#         temp.banner = df.iloc[i]['image']
#         temp.title = df.iloc[i]['title']
#         temp.description = df.iloc[i]['content']
#         temp.save()
# except:
#     pass

# obj = Blog.objects.get(id = 4)
# obj.banner = 'media//blog_banner//thegioi1_6'
# obj.save()
# cate = Category.objects.get(id = 1)
# print(cate)

        

class TextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=True)


class CreateBlogForm(forms.ModelForm):
    # description = RichTextField()
    
    class Meta:
        model = Blog
        fields = (
            "title",
            "category",
            "banner",
            "description"
        )