# coding=utf-8
from simple import MQTTClient
from machine import Pin
import ujson as json
import machine
import micropython
from machine import ADC
from machine import Timer
import urequests

# 选择G4引脚
g4 = Pin(4, Pin.OUT, value=0)
# OneNet  MQTT服务器地址域名为：183.230.40.39,不变
SERVER = "183.230.40.39"
# 设备ID
CLIENT_ID = "24789075"
# 随便起个名字
TOPIC = b"TurnipRobot"
# 产品ID
username = '118117'
# 产品APIKey:
password = 'K9QGuh=BM6s2JjV75mSufbtrqt4='

isTell = True  # 提醒-默认打开
isVoice = False  # 声音-默认关闭
isTellTime = 10  # 关闭提醒时间设置-默认10min
tellTime = isTellTime * 60 / 5  # 副本 有多少个5s
valueOut = 600  # 阈值-默认700


def getTellTime(msg):  # 处理数值信息
    global isTellTime
    global valueOut
    global tellTime
    value = int(msg)
    print(value)
    if value <= 60:  # 设置 不再提醒的时间
        isTellTime = value
        tellTime = isTellTime * 60 / 5
        print('set time OK! isTellTime = ', isTellTime)
    else:  # 阈值设置
        valueOut = value
        print('set valueOut OK! valueOut = ', valueOut)


def sub_cb(topic, msg):  # 接收到数据，进行判断，并执行相应动作
    global isTell
    global isVoice
    global tellTime
    print((topic, msg))
    if msg == b"off":  # 提醒打开
        isTell = True
        tellTime = isTellTime * 60 / 5
        print("opens tell!")
        return True
    elif msg == b"on":  # 关闭提醒
        isTell = False
        tellTime = isTellTime * 60 / 5
        print("close tell! time = ", isTellTime)
        return True
    elif msg == b"voice_on":  # 打开 声音
        isVoice = True
        print("open voice!")
    elif msg == b"voice_off":  # 关闭声音
        isVoice = False
        print("close voice!")
    else:
        getTellTime(msg)  # 判断是否为数值信息


tim_pubDate = Timer(-1)  # 新建一个虚拟定时器,用于上传信息
tim_voice = Timer(-1)  # 新建一个虚拟定时器，用于蜂鸣器的时间设置


def main(server=SERVER):
    # 端口号为：6002
    c = MQTTClient(CLIENT_ID, server, 6002, username, password)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(TOPIC)
    tim_pubDate.init(period=5000, mode=Timer.PERIODIC, callback=lambda t: pubData(c, t))
    pubData(c, 10)
    print("Connected to %s, subscribed to %s topic" % (server, TOPIC))
    try:
        while 1:
            c.wait_msg()
    finally:
        print('mqtt closed')
        c.disconnect()


tim_voice.init(period=2000, mode=Timer.PERIODIC, callback=lambda t: do_voice(t))# 2s定时器
flag_out = False  # 用于判断是否达到阈值
times_out = 0  # 用于限制发送次数


def do_voice(t):  # 每2s调用一次，声音提示
    if flag_out and isVoice:  # 达到阈值并且声音开关打开
        g4.value(not g4.value())  # 蜂鸣器高低电平交替
    else:
        g4.value(0)  # 蜂鸣器变为低电平，不响


def pubData(mqtt, t):# 推送时间
    global flag_out
    global times_out
    global tellTime
    global isTell
    my_data = 1024 - adc.read()
    if my_data >= valueOut:
        times_out += 1
        if times_out % 5 == 1 and tellTime == isTellTime * 60 / 5:  # 每4*5s发一次微信通知
            SendData(my_data)  # 发送微信通知
            print('send data!')
        flag_out = True  # 达到阈值标志位为True
    else:
        times_out = 0  # 清0
        flag_out = False
    if not isTell:
        tellTime -= 1
        if tellTime == 0:
            isTell = True
            tellTime = isTellTime * 60 / 5
    else:
        tellTime = isTellTime * 60 / 5

    value = {'datastreams': [{"id": "temp", "datapoints": [{"value": my_data}]}]}#json数据格式
    jdata = json.dumps(value)
    jlen = len(jdata)
    print(jdata)
    bdata = bytearray(jlen + 3)
    bdata[0] = 1  # publish data in type of json
    bdata[1] = int(jlen / 256)  # data lenght
    bdata[2] = jlen % 256  # data lenght
    bdata[3:jlen + 4] = jdata.encode('ascii')  # json data
    print(bdata)
    try:
        mqtt.publish('$dp', bdata)
    except Exception as ex:
        print('publish failed:', ex.message())


SCKEY = 'SCU20157T6db277da9387b083a0172fe2b21b95b15a5c7cbc75489'


def push(result):
    title = "Ta尿尿啦"
    # content = 'text=' + title + '&' + 'desp=' + result
    # url = "https://sc.ftqq.com/%s.send?%s" % (SCKEY, content)
    url = "http://sc.ftqq.com/webhook/317-5a5ca832003c2?TA_action_on=1&TA_url_a=https://open.iot.10086.cn/app/browse2?openid=9500e25da0fb4636779184a7994949ee&amp;wap=1&f=true&TA_title=%s&TA_content=%s" % (
        title, result)
    print(url)
    r = urequests.request("POST", url)
    try:
        print(r.json())
        if r.json()['errmsg'] == 'success':
            print('send secussfully!')
        else:
            print(r.json['errmsg'])
    except:
        print('send failed!')
    # r = urequests.get(url)
    # r.close()


p2 = Pin(2, Pin.OUT)
adc = ADC(0)


def SendData(data):
    p2.value(not p2.value())
    data_ = "尿量=%d</br>请前去查看</br>来自:智能隔尿垫" % (data)
    print('data_ = ', data_)
    push(data_)
    print('send secussfully!')
