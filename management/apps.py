from django.apps import AppConfig
from suit.apps import DjangoSuitConfig

class ManagementConfig(AppConfig):
    name = 'management'

class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'
