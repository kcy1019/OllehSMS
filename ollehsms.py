# -*- coding: utf-8 -*-
import re
import urllib
import requests as rq
# Since requests doesn't have -*- coding -*-.
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


"""
# OllehSMS

Python API wrapper for Olleh Web SMS Sending Service.

## USAGE

    msg = r'Let's send SMS programatically!'
    sms = OllehSMS()
    print 'auth', sms.auth('my_id', 'some_fancy_strong_password')  # auth True
    print 'send', sms.send(msg, ['010-XXXX-XXXX'])  # send True

"""


class OllehSMS:
    URL_INIT = 'https://login.olleh.com/wamui/AthMobile.do?mRt=https://m.mms.olleh.com/mustmollehweb/msgsend/intro.asp'
    URL_AUTH = 'https://login.olleh.com/wamui/AthMobile.do?mRt=https://m.mms.olleh.com/mustmollehweb/msgsend/intro.asp'
    URL_SEND_ENQUEUE = 'https://m.mms.olleh.com/mustmollehweb/msgsend/div/alertSendBefore.asp'
    URL_SEND_CONFIRM = 'https://m.mms.olleh.com/mustmollehweb/msgSend/send/smsSend_Portal.asp'
    URL_REMAINING_FREE = 'https://m.mms.olleh.com/MustmOllehWeb/msgSend/intro.asp'

    PATTERN_REMAINING_FREE = re.compile(r'freeSmsCnt" value="([0-9]+)"', re.IGNORECASE)
    PATTERN_MY_PHONE = re.compile(r'var _my_phone = "([^"]+)"', re.IGNORECASE)
    DATA_SEND_CONFIRM = r'dispmsg=S&dispmsgType=smsPortal&sendcnt=1&ccnt=0&cmsg=&isReserv=N&cid=0&stamp_cnt=0&evt_cnt=0&ISSMSSTAT=SMS&all_cnt=1'
    __VERSION__ = '0.1'

    def __init__(self):
        self.sess = rq.Session()
        self.sess.get(OllehSMS.URL_INIT)
        self.free = 0

    def auth(self, id, pw):
        auth_payload = {'userId': id,
                        'password': pw,
                        'checkSavedId': 'Y'}
        r = self.sess.post(OllehSMS.URL_AUTH, data=auth_payload)
        response = self.sess.get(OllehSMS.URL_REMAINING_FREE).text
        self.free = OllehSMS.PATTERN_REMAINING_FREE.search(response)
        if not self.free:
            return False
        self.free = int(self.free.group(1))
        return True

    def send(self, msg, recipients):
        if not isinstance(msg, unicode):
            msg = msg.decode('utf-8')
        msg = msg.encode('euc-kr')
        size = len(msg)
        target = ','.join((x.replace('-', '') for x in recipients)) + ','

        msg_payload = {'freeSmsCnt': self.free,
                        'recvCnt': len(recipients),
                        'recvLists': target,
                        'recvNames': target,
                        'msgType': 'SMS',
                        'isGroups': 'N',
                        'authChk': 'OK',
                        'smsSndChk': 'N',
                        'editInput': msg,
                        'dataLen': size,
                        'mmsArea': '<body></body>'}

        r = self.sess.post(OllehSMS.URL_SEND_ENQUEUE, data=msg_payload).text
        r = OllehSMS.PATTERN_MY_PHONE.search(r)
        if not r:
            return False
        else:
            my_phone = r.group(1)

        msg_payload['MsgDetailType'] = 'A00'
        msg_payload['sendhtml'] = msg_payload['editInput']
        msg_payload['recvLists'] = msg_payload['recvLists'].encode('base64')[:-1]
        msg_payload['recvNames'] = msg_payload['recvNames'].encode('base64')[:-1]
        msg_payload['sndIdx'] = msg_payload['isDeco'] = msg_payload['isDecoBg'] = ''
        msg_payload['picIdx'] = msg_payload['PhotoUrl'] = msg_payload['starSMS'] = ''
        msg_payload['reserved'] = msg_payload['autoName'] = msg_payload['cIdx'] = ''
        msg_payload['recvConfirm'] = msg_payload['recvPhone'] = msg_payload['readConfirm'] = ''

        msg_payload_serialized = urllib.urlencode(msg_payload)
        msg_payload_serialized += '&sendPhone=' + my_phone

        self.sess.post(OllehSMS.URL_SEND_CONFIRM, data=msg_payload_serialized,
                headers={"Content-Type":
                         "application/x-www-form-urlencoded  charset=euc-kr",
                         "X-Project": "pcMessenger",
                         "X-Version": "1.0.1",
                         "X-Request-With": "XMLHttpRequest"})
        return True
