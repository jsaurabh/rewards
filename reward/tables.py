import django_tables2 as tables
from django_tables2 import TemplateColumn

class CurrencyTable(tables.Table):
    business = tables.Column(verbose_name = 'Business Name')
    label = tables.Column(verbose_name= 'Label')
    class Meta:
        template_name = "django_tables2/bootstrap-responsive.html"

class CampaignTable(tables.Table):
    name = tables.Column(verbose_name= 'Campaign Name')
    start = tables.Column(verbose_name= 'Start Date')
    end = tables.Column(verbose_name= 'End Date')
    expiry = tables.Column(verbose_name= 'Points Expiry')
    business = tables.Column(verbose_name = 'Business Name')
    currency = tables.Column(verbose_name= 'Currency Name')
    
    class Meta:
        template_name = "django_tables2/bootstrap-responsive.html"

class AccRulesTable(tables.Table):
    value = tables.Column(verbose_name= 'Value($)')
    campaign = tables.Column(verbose_name= 'Campaign')
    category = tables.Column(verbose_name= 'Category')
    item = tables.Column(verbose_name= 'Item')
    
    class Meta:
        template_name = "django_tables2/bootstrap-responsive.html"

class RedRulesTable(tables.Table):
    reward = tables.Column(verbose_name= 'Reward ')
    #image = tables.Column(verbose_name= 'Campaign ID')
    value = tables.Column(verbose_name= 'Dollar Spend')
    campaign = tables.Column(verbose_name= 'Campaign ID')
    
    class Meta:
        template_name = "django_tables2/bootstrap-responsive.html"