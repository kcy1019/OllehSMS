# OllehSMS

Python API wrapper for KT(Olleh) Web SMS Sending Service.

## USAGE

    msg = u'Let's send SMS programatically!'
    sms = OllehSMS()
    print 'auth', sms.auth('my_id', 'some_fancy_strong_password')
    print 'send', sms.send(msg, ['010-XXXX-XXXX'])

