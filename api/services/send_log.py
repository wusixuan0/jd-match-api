from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# TODO: move to util folder
channel_layer = get_channel_layer()

def send_log(message):
    async_to_sync(channel_layer.group_send)(
        "log_group",
        {
            'type': 'send_log_update',
            'log_entry': message
        }
    )