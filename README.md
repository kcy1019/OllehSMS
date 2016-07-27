# Olleh SMS API Wrapper

## Auth(get cookie)
POST https://login.olleh.com/wamui/AthMobile.do?mRt=https://m.mms.olleh.com/mustmollehweb/msgsend/intro.asp

userId={id}&password={pass}&checkSavedId=Y.format(...)

## Send Message

### Immediate Send
POST https://m.mms.olleh.com/mustmollehweb/msgsend/div/alertSendBefore.asp
freeSmsCnt: 82(you should parse it from or ...?)
recvCnt: 1 (length of the array)
recvLists: (Phone number,)+
recvNames: =recvLists
msgType: SMS
isGroups: N
authChk: OK
smsSndChk: N
editInput: (msg-content).encode('euc-kr')
dataLen: =editInput.length
mmsArea: '<body></body>'

POST https://m.mms.olleh.com/mustmollehweb/msgsend/div/alertSendAfter.asp
dispmsg=S&dispmsgType=smsPortal&sendcnt=1&ccnt=0&cmsg=&isReserv=N&cid=0&stamp_cnt=0&evt_cnt=0&ISSMSSTAT=SMS&all_cnt=1

### Scheduled Send


