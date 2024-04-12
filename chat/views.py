# # from django.shortcuts import render
# #
# # from .models import Message
# #
# #
# # def chat_room(request, room_name):
# #     room = Room.objects.get(name=room_name)
# #     messages = Message.objects.filter(room=room)
# #
# #     context = {
# #         'data': {
# #             'title': room.name,
# #         },
# #         'room_name': room_name,
# #         'messages': messages,
# #     }
# #     return render(request, 'chat.html', context)
# #

from django.shortcuts import redirect
from django.views.generic import View
# chat/views.py

from django.shortcuts import render

from django.urls import reverse

#
# def room(request, room_name):
#     return render(request, 'chat/chat.html', {
#         'room_name': room_name
#     })



def room(request):
    room_name = "название_комнаты"

    room_url = reverse('room', args=[room_name])
    return render(request, 'chat/chat.html', {'room_url': room_url})

# class JoinChatView(View):
#     def get(self, request, room_name):
#         # Перенаправляем пользователя на URL комнаты с использованием именованного URL
#         return redirect('join_chat', room_name=room_name)

# from django.shortcuts import redirect
# from django.views.generic.base import View
# from .models import Room
#
#
# class JoinChatView(View):
#     def get(self, request):
#         # Получаем текущий объект ObjIdfDialog для пользователя
#         obj_idf_dialog = request.user.identification_dialog
#
#         # Если объект ObjIdfDialog не существует, выполните действие по умолчанию
#         if not obj_idf_dialog:
#             return redirect('default_route')
#
#         # Получаем последнюю созданную комнату для текущего объекта ObjIdfDialog
#         room = Room.objects.filter(host=obj_idf_dialog).order_by('-created_at').first()
#
#         if room:
#             # Если комната найдена, перенаправляем пользователя на URL этой комнаты
#             return redirect('chat_room', room_name=room.name)
#         else:
#             # Если комната не найдена, можно выполнить действие по умолчанию
#             return redirect('default_route')
#
# from django.shortcuts import redirect
# from django.utils import timezone
# from django.views.generic.base import View
#
# from .models import Room
#
