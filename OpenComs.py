import pickle
from twilio.rest import Client
from flask import Flask, request
import openai
import config
from config import other_number, API_numbers, API_numbers_reversed

# Load assignments created by Assign.py
name_phone, phone_name, santa_child, child_santa = pickle.load(open('assignments', 'rb'))

openai.api_key = config.openai_api_key


def baby_talk(text):
    """
    Uses OpenAI's GPT-3 Davinci model to 'translate' text to a toddler's manner of speaking.
    :param text: Text to be translated
    :return: Translated text
    """
    start_sequence = "\nBaby talk:"
    if text[-1] != '.':
        text += '.'

    response = openai.Completion.create(
        engine="davinci",
        prompt="The following are baby-talk versions of things we say every day.\n\nRegular: I fell down and scraped "
               "my elbow.\nBaby talk: goo goo gaga I got an owie on my elbow.\n\nRegular: I am scared.\nBaby talk: I "
               "a wittle scawed.\n\nRegular: I have a stomach ache.\nBaby talk: Me have a boo boo tummy.\n\nRegular: "
               "little.\nBaby talk: wittle ittle.\n\nRegular: This is delicious.\nBaby talk: Yummy tummy.\n\nRegular: "
               "I need to leave soon.\nBaby talk: me go bye bye.\n\nRegular: " + text,
        temperature=0.7,
        max_tokens=468,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        start_sequence=start_sequence
    )
    return response['choices'][0]['text'].replace('\nBaby talk:', '').lstrip()


def santa_talk(text):
    """
    Uses OpenAI's GPT-3 Davinci model to 'translate' text to santa's manner of speaking.
    :param text: Text to be translated
    :return: Translated text
    """
    response = openai.Completion.create(
        engine="davinci",
        prompt="Santa says \"Hello\" like \"Ho, ho, ho. Merry Christmas!\".  Santa says \"What do you want for "
               "Christmas?\" like \"ho ho ho. Now, what would you like for Christmas?\". Santa says \"you have been "
               "good\" like \"My elves have told me you have been very good this year\". Santa says \"I got you "
               "something you can wear\" like \"Now, I have something for you to wear\". Santa says \"" + text + "\" "
                                                                                                                 "like \"",
        temperature=0.7,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\""]
    )
    return response['choices'][0]['text']


client = Client(config.account_sid, config.auth_token)



def send_message(person, body_text, format):
    if format == 'to santa':
        body_text = santa_talk(body_text.strip())
        to_send = f'Santa: {body_text}'
        confirmation = f"You: {body_text}"
        to_person = santa_child[person]
    if format == 'to child':
        body_text = baby_talk(body_text.strip())
        to_send = f'{person}: {body_text}'
        confirmation = f"You: {body_text}"
        to_person = child_santa[person]
    message = client.messages \
        .create(
        body=confirmation,
        from_=API_numbers[format.split(' ')[1]],
        to=name_phone[person]
    )
    message = client.messages \
        .create(
        body=to_send,
        from_=other_number[API_numbers[format.split(' ')[1]]],
        to=name_phone[to_person]
    )
    return message


def incoming_msg(number, body_text, to):
    person = phone_name[number]
    com_line = API_numbers_reversed[to]
    if com_line == 'santa':
        message = send_message(person, body_text, 'to santa')

    elif com_line == 'child':
        message = send_message(person, body_text, 'to child')

    return message


app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    number = request.form['From']
    message_body = request.form['Body']
    to = request.form['To']

    message = incoming_msg(number, message_body, to)

    return str(message)


# send opening text
body = 'Texting is now online'

for santa, child in santa_child.items():
    client.messages.create(body=body,
                           from_=API_numbers['santa'],
                           to=name_phone[santa])
    client.messages.create(body=body,
                           from_=API_numbers['child'],
                           to=name_phone[santa])

if __name__ == "__main__":
    app.run(debug=False)
