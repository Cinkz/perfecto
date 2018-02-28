from __future__ import unicode_literals

from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from channel.models.core.model import Channel
from channel.views.core.mixin import ChannelRootMixin, MyChannelRootMixin
from dialogue.models.core.model import Dialogue
from dialogue.models.core.serializer import DialogueSerializer
from transaction.models.core.model import Transaction


class NestedDialogueViewSet(ChannelRootMixin, viewsets.ModelViewSet):
    queryset = Dialogue.objects.all()
    serializer_class = DialogueSerializer

class MyNestedDialogueViewSet(MyChannelRootMixin, viewsets.ModelViewSet):
    queryset = Dialogue.objects.all()
    serializer_class = DialogueSerializer

    def list(self, request, *args, **kwargs):
        channel = self.get_channel()
        channel_user_instance = channel.channel_user_set.get(user=request.user)
        channel_user_instance.unread_message_count = 0
        channel_user_instance.save()
        return super(MyNestedDialogueViewSet, self).list(request, *args, **kwargs)

    @detail_route(methods=['post'])
    def resolve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.event.get('type', None) == 'task' and request.data.get('action', None) == 'accept':
            channel = Channel.objects.create(
                type=Channel.TASK,
                users=[
                    {'user': {'id': instance.created_by.id}, 'alias': instance.data['topic']},
                    {'user': {'id': request.user.id}, 'alias': instance.data['topic']},
                ])
            Dialogue.objects.create(
                channel=instance.channel,
                event={'type': 'channel', 'channel': {'id': channel.id, 'alias': instance.data['topic']}, 'action': 'create'},
                created_by=request.user,
            )
            instance.data['accepted'] = True
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        elif instance.event.get('type', None) == 'invoice' and request.data.get('action', None) == 'pay':
            transaction = Transaction.objects.create(
                dialogue=instance,
                channel=request.data['channel'],
                amount=instance.data['amount'],
                ipv4=request.ipv4,
            )
            transaction.get_charge_object()
            return Response({
                'amount': transaction.charge['amount'],
                'channel': transaction.charge['channel'],
                'qrcode': transaction.charge['credential'][transaction.charge['channel']],
            })

        return Response(status=status.HTTP_200_OK)
