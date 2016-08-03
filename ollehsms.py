# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import sys
import urllib
import codecs
import requests as rq


"""
# OllehSMS

Python API wrapper for KT(Olleh) Web SMS Sending Service.

## USAGE

    from ollehsms import OllehSMS

    msg = u'Let\'s send SMS programatically!'
    sms = OllehSMS()
    print 'auth', sms.auth('my_id', 'some_fancy_strong_password')
    print 'send', sms.send(msg, ['010-XXXX-XXXX'])

"""

if sys.stdout.encoding != 'UTF-8':
    print('Please set PYTHONENCODING=UTF-8 in your environment then retry.', file=sys.stdout)


class OllehSMS:
    URL_INIT = 'https://login.olleh.com/wamui/AthMobile.do?mRt=https://m.mms.olleh.com/mustmollehweb/msgsend/intro.asp'
    URL_AUTH = 'https://login.olleh.com/wamui/AthMobile.do?mRt=https://m.mms.olleh.com/mustmollehweb/msgsend/intro.asp'
    URL_SEND_ENQUEUE = 'https://m.mms.olleh.com/mustmollehweb/msgsend/div/alertSendBefore.asp'
    URL_SEND_CONFIRM = 'https://m.mms.olleh.com/mustmollehweb/msgSend/send/smsSend_Portal.asp'
    URL_REMAINING_FREE = 'https://m.mms.olleh.com/MustmOllehWeb/msgSend/intro.asp'

    PATTERN_REMAINING_FREE = re.compile(r'freeSmsCnt" value="([0-9]+)"', re.IGNORECASE)
    PATTERN_MY_PHONE = re.compile(r'var _my_phone = "([^"]+)"', re.IGNORECASE)

    SMS_MAXIMUM_LENGTH = 73

    __version__ = '0.1'

    def __init__(self):
        self.sess = rq.Session()
        self.sess.get(OllehSMS.URL_INIT)
        self.free = 0

    def auth(self, id, pw):
        """Login and prepare for sending SMS.
        Args:
            id (str): olleh.com ID.
            pw (str): olleh.com password.

        Returns:
            bool: True if successful, False otherwise.
        """
        auth_payload = {'userId': id,
                        'password': pw,
                        'checkSavedId': 'Y'}
        self.sess.get(OllehSMS.URL_INIT)
        self.sess.post(OllehSMS.URL_AUTH, data=auth_payload)

        response = self.sess.get(OllehSMS.URL_REMAINING_FREE).text
        self.free = OllehSMS.PATTERN_REMAINING_FREE.search(response)

        if not self.free:
            return False
        self.free = int(self.free.group(1))

        return True

    def send(self, msg, recipients):
        if hasattr(str, 'decode') and not isinstance(msg, unicode):
            msg = msg.decode('utf-8')  # Python 2
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

        if size > OllehSMS.SMS_MAXIMUM_LENGTH:
            msg_payload['msgType'] = 'LTS'

        r = self.sess.post(OllehSMS.URL_SEND_ENQUEUE, data=msg_payload).text
        r = OllehSMS.PATTERN_MY_PHONE.search(r)

        if not r:
            return False
        else:
            my_phone = r.group(1)

        msg_payload['MsgDetailType'] = 'A00'
        confirm_url = OllehSMS.URL_SEND_CONFIRM
        self.free -= 1

        if size > OllehSMS.SMS_MAXIMUM_LENGTH:  # In case of LMS
            msg_payload['MsgDetailType'] = 'D00'
            confirm_url = OllehSMS.URL_SEND_CONFIRM.replace('smsSend', 'mmsSend')
            self.free -= 1  # LMS consumes additional Free SMS count.

        msg_payload['sendhtml'] = msg_payload['editInput']

        if hasattr(urllib, 'urlencode'):  # Python 2
            msg_payload['recvLists'] = msg_payload['recvLists'].encode('base64')[:-1]
            msg_payload['recvNames'] = msg_payload['recvNames'].encode('base64')[:-1]
            msg_payload_serialized = urllib.urlencode(msg_payload)
        else:  # Python 3
            msg_payload['recvLists'] = codecs.encode(bytes(msg_payload['recvLists'], 'ascii'), 'base64')
            msg_payload['recvNames'] = codecs.encode(bytes(msg_payload['recvNames'], 'ascii'), 'base64')
            msg_payload_serialized = urllib.parse.urlencode(msg_payload)

        msg_payload_serialized += '&sendPhone=' + my_phone

        self.sess.post(confirm_url, data=msg_payload_serialized,
                       headers={"Content-Type":
                                "application/x-www-form-urlencoded  charset=euc-kr",
                                "X-Project": "pcMessenger",
                                "X-Version": "1.0.1",
                                "X-Request-With": "XMLHttpRequest"})

        # TODO: Check result.
        return True
