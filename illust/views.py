from django.shortcuts import render,redirect
from django.views import View

#ビュークラスに継承させることで、認証状態をチェックする
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Design
from .forms import DesignForm

import magic

ALLOWED_MIME    = [ "image/vnd.adobe.photoshop","application/pdf","application/postscript" ]
AMOUNT          = 20



class illustView(View):

    def get(self, request, *args, **kwargs):

        #Designクラスを使用し、DBへアクセス。order_by("-date")で新しい順、[:数字]で指定した量だけ表示できる
        designs = Design.objects.order_by("-date")[:AMOUNT]


        #filter()で絞り込みができる
        photoshops      = Design.objects.filter(mime="image/vnd.adobe.photoshop").order_by("-date")[:AMOUNT]
        illustrators    = Design.objects.filter(mime="application/postscript"   ).order_by("-date")[:AMOUNT]
        pdfs            = Design.objects.filter(mime="application/pdf"          ).order_by("-date")[:AMOUNT]

        context = { "designs"       : designs,
                    "photoshops"    : photoshops,
                    "illustrators"  : illustrators,
                    "pdfs"          : pdfs,
                   }

        return render(request,"illust/index.html",context)


index   = illustView.as_view()



#LoginRequiredMixinでログイン状態をチェック、認証状態にあればアクセスを許可する。
class uploadView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):


        return render(request, "illust/upload.html")

    def post(self, request, *args, **kwargs):


        if "file" not in request.FILES:
            return redirect("illust:index")

        mime_type = magic.from_buffer(request.FILES["file"].read(1024), mime=True)
        print(mime_type)

        copied          = request.POST.copy()
        copied["mime"]  = mime_type
        copied["user"]  = request.user.id #←ユーザーIDをセットする

        form = DesignForm(copied, request.FILES)

        if form.is_valid():
            print("バリデーションOK ")
            if mime_type in ALLOWED_MIME:
                result  = form.save()
            else:
                print("このファイルは許可されていません")
                return redirect("illust:upload")
        else:
            print("バリデーションNG")
            return redirect("illust:upload")

        return redirect("illust:upload")

upload  = uploadView.as_view()
