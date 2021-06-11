from django.contrib import admin
from django.utils.html import format_html


from .models import Design

#↑モデルインポート。↓インポートしたモデルを管理サイトで扱う

class DesignAdmin(admin.ModelAdmin):


    #指定したフィールドを表示、編集ができる
    list_display        = [ "title","date","mime","format_thumbnail","error","format_user" ]
    #list_editable       = [ "error" ]


    #指定したフィールドの検索と絞り込みができる
    search_fields       = [ "title","description" ]
    list_filter         = [ "mime","error","user" ]


    #1ページ当たりに表示する件数、全件表示を許容する最大件数(ローカルでも5000件を超えた辺りから遅くなるので、10000~50000辺りが無難)
    list_per_page       = 10
    list_max_show_all   = 20000

    #日付ごとに絞り込む、ドリルナビゲーションの設置
    date_hierarchy      = "date"


    #画像のフィールドはimgタグで画像そのものを表示させる
    def format_thumbnail(self,obj):
        if obj.thumbnail:
            return format_html('<img src="{}" alt="画像" style="width:5rem;height:5rem;">', obj.thumbnail.url)

    #画像を表示するときのラベル(thumbnailのverbose_nameをそのまま参照している)
    format_thumbnail.short_description      = Design.thumbnail.field.verbose_name
    format_thumbnail.empty_value_display    = "画像なし"


    #投稿者の表示。外部キーuserのidを使い、カスタムユーザーモデルのfirst_name及びlast_nameを表示
    def format_user(self,obj):
        if obj.user.first_name and obj.user.last_name:
            return obj.user.last_name + " " + obj.user.first_name

    format_user.short_description      = Design.user.field.verbose_name
    format_user.empty_value_display    = "名前がありません"
    



#DesignAdminを第二引数に指定
admin.site.register(Design,DesignAdmin)
