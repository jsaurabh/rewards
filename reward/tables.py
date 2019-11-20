import django_tables2 as tables
from django_tables2 import TemplateColumn

class CurrencyTable(tables.Table):
    id = tables.Column(verbose_name= 'Currency ID' )
    singular = tables.Column(verbose_name= 'Singular')
    plural = tables.Column(verbose_name= 'Plural')

    business = tables.Column(verbose_name = 'Business ID')
    class Meta:
        template_name = "django_tables2/bootstrap-responsive.html"

class CampaignTable(tables.Table):
    id = tables.Column(verbose_name= 'Campaign ID' )
    name = tables.Column(verbose_name= 'Campaign Name')
    start = tables.Column(verbose_name= 'Start Date')
    end = tables.Column(verbose_name= 'End Date')
    expiry = tables.Column(verbose_name= 'Points Expiry')
    business = tables.Column(verbose_name = 'Business ID')
    currency = tables.Column(verbose_name= 'Currency ID')
    
    class Meta:
        template_name = "django_tables2/bootstrap-responsive.html"

class AccRulesTable(tables.Table):
    id = tables.Column(verbose_name= 'Rule ID' )
    value = tables.Column(verbose_name= 'Spend($)')
    campaign = tables.Column(verbose_name= 'Campaign ID')
    category = tables.Column(verbose_name= 'Category ID')
    item = tables.Column(verbose_name= 'Item ID')
    
    class Meta:
        template_name = "django_tables2/bootstrap-responsive.html"

class RedRulesTable(tables.Table):
    id = tables.Column(verbose_name= 'Rule ID' )
    reward = tables.Column(verbose_name= 'Reward ')
    #image = tables.Column(verbose_name= 'Campaign ID')
    value = tables.Column(verbose_name= 'Dollar Spend')
    campaign = tables.Column(verbose_name= 'Campaign ID')
    
    class Meta:
        template_name = "django_tables2/bootstrap-responsive.html"