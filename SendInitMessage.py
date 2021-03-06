# Uses participants and assignments from saved pickle to send an initial message explaining how the system works and their assinged person.

import pickle
import config
from twilio.rest import Client

# Load assignments created by Assign.py
name_phone, phone_name, santa_child, child_santa = pickle.load(open('assignments', 'rb'))

client = Client(config.account_sid, config.auth_token)


def init_message_santa(person, child):
    return f"Hello {person}, this year your child is **{child}**. You can text them here. You can see their name, " \
           f"but they can't see yours. Your texts are translated to sound like santa when you send them. You will see " \
           f"the translation after sending. "


def init_message_child():
    return f"This is a chat with your Secret Santa. They can see your name, but you can't see theirs. Your texts are " \
           f"translated to sound like a toddler when you send them. You will see the translation after sending. "


for santa, child in santa_child.items():
    client.messages.create(body=init_message_santa(santa, child),
                           from_=config.API_numbers['santa'],
                           to=name_phone[santa])
    client.messages.create(body=init_message_child(),
                           from_=config.API_numbers['child'],
                           to=name_phone[santa])
