from twilio.rest import Client
# Your Twilio account SID and authentication token
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
# Create a Twilio client
client = Client(account_sid, auth_token)
# The call SID of the call to turn
call_sid = 'your_call_sid'
# The phone number to turn the call to
to_number = 'destination_phone_number'
# Turn the call to the destination number
call = client.calls(call_sid).update(
    twiml='<Response><Dial>'+to_number+'</Dial></Response>'
)
print("Call SID:", call.sid)
