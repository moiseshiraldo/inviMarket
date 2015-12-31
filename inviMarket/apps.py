# -*- coding: utf-8 -*-
from django.apps import AppConfig

class inviMarketConfig(AppConfig):
    name = 'inviMarket'

    def ready(self):
        import inviMarket.signals