from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from django.db.models import Max

from .models import ChatRoom
from product.models import Product
from .forms import NewMessageForm

# Create your views here.

@csrf_exempt
@login_required
def new_chatroom(request, product_pk):
    product = get_object_or_404(Product, id=product_pk)

    chatroom = ChatRoom.objects.filter(product=product).filter(members__in=[request.user.id])

    if chatroom:
        return redirect('chat:chatroom', chatroom_pk = chatroom.first().id)

    if request.method == 'POST':
        form = NewMessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sent_by = request.user
            message.save()

            chatroom = ChatRoom.objects.create(product=product)
            chatroom.members.add(request.user)
            chatroom.members.add(product.created_by)
            chatroom.messages.add(message)
            chatroom.save()

            return redirect('chat:chatroom', chatroom_pk=chatroom.id)
    
    else:
        form = NewMessageForm()

    return render(request, 'chat/new_chatroom.html', {
        'form': form,
        'title': 'New Chatroom',
    })


@login_required
def chatroom(request, chatroom_pk):
    chatroom = get_object_or_404(ChatRoom, id=chatroom_pk)
    form = NewMessageForm()

    return render(request, 'chat/chatroom.html', {
        'chatroom': chatroom,
        'form': form,
        'title': 'ChatRoom',
    })


@login_required
def inbox(request):
    chatrooms = ChatRoom.objects.filter(members__in=[request.user.id]).annotate(latest_message_time=Max('messages__created_at')).order_by('-latest_message_time')

    return render(request, 'chat/inbox.html', {
        'chatrooms': chatrooms,
        'title': 'Inbox',
    })

