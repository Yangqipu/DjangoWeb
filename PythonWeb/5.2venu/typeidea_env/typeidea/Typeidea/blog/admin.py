from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from django.contrib import admin
from Typeidea.custom_site import custom_site
from Typeidea.base_admin import BaseOwnerAdmin


@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    # inlines = [PostInline]
    list_display = ("name", "status", "is_nav", "created_time")
    fields = ("name", "status", "is_nav")



@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ("name", "status", "created_time")
    fields = ("name", "status")

class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""
    title = "分类过滤器"
    parameter_name = "owner_category"

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list("id", "name")

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""
    title = "分类过滤器"
    parameter_name = "owner_category"

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list("id", "name")

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        "title", "category", "status", "created_time","owner","operator"
    ]
    list_display_links = []
    exclude = ["owner", ]
    # list_filter = ["category", ]
    list_filter = [CategoryOwnerFilter]
    search_fields = ["title", "category_name"]
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = "操作"

    # def get_queryset(self,request):
    #     qs=super(PostAdmin,self).get_queryset(request)
    #     return qs.filter(owner=request.user)

    class Media:
        css = {
            "all": ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
        }
        js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js")


@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display=["object_repr","object_id","action_flag","user","change_message"]
