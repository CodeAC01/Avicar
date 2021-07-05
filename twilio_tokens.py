from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC1fe7806320fec11b13952423cfc2d8e1'
auth_token = '35ee0969da5c5690dda126984892ffde'
client = Client(account_sid, auth_token)

token = client.tokens.create()

print(token.ice_servers)