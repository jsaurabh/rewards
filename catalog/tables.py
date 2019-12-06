import django_tables2 as tables
from django_tables2 import TemplateColumn

#from .forms import BusinessEditForm

class CategoryTable(tables.Table):
    name = tables.Column()
    items = TemplateColumn(template_code='<a class="btn btn-primary btn-icon-split btn-sm" href = "items" ><span class="icon text-white-50"><i class="fas fa-edit"></i></span><span class="text">View</span></a>')
    #edit = TemplateColumn(template_code='<a class="btn btn-primary btn-icon-split btn-sm" href = "edit" ><span class="icon text-white-50"><i class="fas fa-edit"></i></span><span class="text">Edit</span></a>')
    #delete = TemplateColumn(template_code='<a class="btn btn-primary btn-icon-split btn-sm" href = "delete" ><span class="icon text-white-50"><i class="fas fa-edit"></i></span><span class="text">Delete</span></a>')
    class Meta:
        template_name = "django_tables2/bootstrap-responsive.html"

class ItemTable(tables.Table):
    name = tables.Column(verbose_name= 'Item Name')
    #items = tables.Column(verbose_name= 'Item')
    category = tables.Column(verbose_name = 'Category Name')
    #TemplateColumn(template_code='<a class="btn btn-primary btn-icon-split btn-sm" href = "items" ><span class="icon text-white-50"><i class="fas fa-edit"></i></span><span class="text">View</span></a>')
    #edit = TemplateColumn(template_code='<a class="btn btn-primary btn-icon-split btn-sm" href = "edit" ><span class="icon text-white-50"><i class="fas fa-edit"></i></span><span class="text">Edit</span></a>')
    #delete = TemplateColumn(template_code='<a class="btn btn-primary btn-icon-split btn-sm" href = "delete" ><span class="icon text-white-50"><i class="fas fa-edit"></i></span><span class="text">Delete</span></a>')
    class Meta:
        template_name = "django_tables2/bootstrap-responsive.html"