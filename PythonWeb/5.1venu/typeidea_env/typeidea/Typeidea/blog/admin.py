from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from django.contrib import admin
from Typeidea.custom_site import custom_site

# Register your models here.

# StackedInline
class PostInline(admin.TabularInline):
    fields = ("title", "desc")
    # 控制额外多几个
    extra = 1
    model = Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # inlines = [PostInline]
    list_display = ("name", "status", "is_nav", "created_time", "owner")
    fields = ("name", "status", "is_nav")

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, form, obj, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "created_time")
    fields = ("name", "status")

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, form, obj, change)


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
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = [
        "title", "category", "status", "created_time", "operator"
    ]
    list_display_links = []
    exclude = ("owner",)
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

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, form, obj, change)
