from django.shortcuts import render

def show_index(req):

    data = {
        'title': 'Чаты'
    }

    return render(req, 'server/chat.html', data)