# from celery import shared_task
from time import sleep
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import requests


# @shared_task
def sleepy():
    print("hellopartner")


# @shared_task(serializer = 'json')
def SendMail(from_email, to_list, dic, template):

    subject, from_email, to = dic['subject'], from_email, to_list
    message = render_to_string(template, dic)
    email = EmailMessage(subject, message , from_email, to)
    if dic['account'] is not None: 
        email.content_subtype = "html"
    
    if dic['attach_filename'] is not None:
        email.attach_file(dic['attach_filename'])

    email.send()
    print("mesasge sent")





# @shared_task(serializer = 'json')
# def SendMessage(reqUrl, apiKey, secretKey, userType, phoneNo, senderId, textMessage):
#     req_params = {
#         'apiKey': apiKey,
#         'secret': secretKey,
#         'userType': userType,
#         'phone': phoneNo,
#         'message': textMessage,
#         'semderid': senderId,
#     }
#     return requests.post(reqUrl, req_params)

