from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather, Say, Hangup, Dial
from flask import Flask, request, Response

app = Flask(__name__)

ACCOUNT_SID = '##############################'
AUTH_TOKEN = '##############################'
TWILIO_PHONE_NUMBER = '+######################'

# Replace with the desired phone number
FORWARD_TO_PHONE_NUMBER = '+4915735989005'

client = Client(ACCOUNT_SID, AUTH_TOKEN)
# response = VoiceResponse()


@app.route('/', methods=['POST'])
def handle_call():
    print('/////////////////')
    response = VoiceResponse()
    gather = Gather(numDigits=1, action='/handle-input', method='POST')
    gather.say(
        "Thank you for calling. If you want to place an online order, press 1. Press 0 to forward the call.")
    response.append(gather)
    return str(response)


@app.route('/handle-input', methods=['POST'])
def handle_input():
    response = VoiceResponse()
    print('..............')
    digit_pressed = request.form['Digits']

    if digit_pressed == '1':
        print('sssssssssssssss')
        send_order_link_sms(request.form['From'])  # Corrected this line
    elif digit_pressed == '0':
        print('ddddd>>>>>>>>')
        dial = response.dial()
        dial.number(FORWARD_TO_PHONE_NUMBER)

    return str(response)


def send_order_link_sms(customer_number):
    print('sms..........')
    order_link = "https://example.com/order"  # Replace with your order link

    message = client.messages.create(
        body=f"Click this link to place your online order: {order_link}",
        from_=TWILIO_PHONE_NUMBER,
        to=customer_number
    )


def forward_call(customer_number):
    print('forward>>>>>>>>')
    response = VoiceResponse()
    dial = Dial(caller_id=TWILIO_PHONE_NUMBER)
    dial.number(FORWARD_TO_PHONE_NUMBER)
    response.append(dial)

    print(response)  # Print the TwiML response to see if it's correctly configured
    call = client.calls.create(
        twiml='<Response><Say>Hello from Twilio!</Say></Response>',
        to=FORWARD_TO_PHONE_NUMBER,
        from_=TWILIO_PHONE_NUMBER
    )
    return call.sid


if __name__ == '__main__':
    app.run(debug=True)
