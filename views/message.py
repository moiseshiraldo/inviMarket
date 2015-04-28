# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View

class MessageView(View):
    message = ""

    def get(self, request):
        return render(request, 'message.html', {'message': self.message})