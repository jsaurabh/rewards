import django_tables2 as tables
from django_tables2 import TemplateColumn

#from .forms import BusinessEditForm

class NameTable(tables.Table):
    
    name = tables.Column()
    phone = tables.Column()
    url = tables.Column()
    address = tables.Column()
    is_published = tables.BooleanColumn(yesno='Yes,No')
    #edit = TemplateColumn(template_code='<a class="btn btn-primary btn-icon-split btn-sm" href = "edit" ><span class="icon text-white-50"><i class="fas fa-edit"></i></span><span class="text">Edit</span></a>')
    #delete = TemplateColumn(template_code='<a class="btn btn-primary btn-icon-split btn-sm" href = "delete" ><span class="icon text-white-50"><i class="fas fa-trash"></i></span><span class="text">Delete</span></a>')
    class Meta:
        template_name = "django_tables2/bootstrap-responsive.html"

#data-toggle="modal" data-target="#editModal"