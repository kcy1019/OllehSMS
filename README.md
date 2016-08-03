# OllehSMS

Python2/3 API wrapper for KT(Olleh) Web SMS Sending Service.

## USAGE
    from ollehsms import OllehSMS
    
    msg = u'Let's send SMS programatically!'
    sms = OllehSMS()
    print('auth-result:', sms.auth('my_id', 'some_fancy_strong_password'))
    print('send-result:', sms.send(msg, ['010-XXXX-XXXX']))
