# OllehSMS

Python API wrapper for KT(Olleh) Web SMS Sending Service.

## USAGE

    from ollehsms import OllehSMS

    msg = u'Let\'s send SMS programatically!'
    sms = OllehSMS()
    print 'auth', sms.auth('my_id', 'some_fancy_strong_password')
    print 'send', sms.send(msg, ['010-XXXX-XXXX'])

## CAUTION

- It is not yet tested on sending to multiple recipients case(but sending one-by-one multiple times is tested for >7 days).
- It only supports prepaid SMS(you can charge them [here][charge]), not pay-on-sending ones.
- If you send 300 SMS during one day(24h), you'll need to unblock your account by manually sending a SMS [here][send].
- KT (basically) does not allow you to send more than 500 SMS in one day(24h).

[charge]: http://mms.mobile.olleh.com/MustOllehWeb/msgSave/start.asp
[send]: http://mms.mobile.olleh.com/MustOllehWeb/msgSend/start.asp
