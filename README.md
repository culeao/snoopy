# 智能隔尿垫


----------


#### [点击查看效果](https://open.iot.10086.cn/app_editor/#/view?openid=9500e25da0fb4636779184a7994949ee&amp%3Bwap=1&f=true)


----------


>该设计是使用NodeMCU，雨滴传感器，蜂鸣器实现的物联网小型项目，可以实时上传婴儿或老人的小便状态，通知监护人及时更换尿垫。


----------


## 功能介绍
* Wife模块使用MQTT通信方式，实时上传到[**OenNet**](https://open.iot.10086.cn/)服务器，并进行数据可视化
* 超过设定阈值自动发到微信端，微信公众号使用第三方-[**Sever酱**](http://sc.ftqq.com/3.version)(从服务器推报警和日志到手机的工具)
* 可以在线设置提醒时间，选择是否声音提醒，设置提醒阈值等
## 程序说明
* `boot.py `——为NodeMCU开机时固定执行代码
* `main.py` ——主函数
* `mqtt.py `——主要逻辑处理程序
* `simple.py` ——网上找的一个mqtt库
## 效果照片
![硬件效果图](https://img-blog.csdn.net/20180423231553603?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDM4NjM2/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
![二维码查看设备详情](https://img-blog.csdn.net/20180423231622879?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDM4NjM2/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
![微信消息通知](https://img-blog.csdn.net/20180423231638107?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDM4NjM2/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
![微信消息详情](https://img-blog.csdn.net/20180423231649493?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDM4NjM2/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
![应用详情](https://img-blog.csdn.net/20180423231702946?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDM4NjM2/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)