#user, password and imap url for an account which raspberry pi will listen for incoming emails
user = 'Username here'
password = 'Your password here'
imap_url = 'Imap url here'

#what folder to look emails for in.
label = 'Inbox'

#Email address from which you will send requests to raspi listening email.
incomingfrom = 'incoming from user here (your personal emai)'

#smtp port and url from which ras pi will send emails
#(we assume raspi listens to and sends eamil from same account, so same username and password from imap will be used).
smtp_url = 'smtp url here'
smtp_port = '465'

#Application will check emails for below trigger message. If it's inside the email and comes from correct person, it will send reply.
triggermessage = "who is there"

#If you want to replace welcoming audio, put your audio into directory and change audio name below.
welcoming_music = "welcoming.mp3"

#if your ip starts with something else than 192, replace the value below.
ip_beginning = "192"
