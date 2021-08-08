# JimnyRC
## 小米遥控车吉姆尼改装  
使用XBOX手柄,通过数莓派4B遥控小米吉姆尼  
在原装底盘上只增加了一个电机驱动模块  

2020版的XBOX手柄(电池仓标签标有Model:1914)连接Linux系统可能会出现重复断开和连接的问题  
https://github.com/atar-axis/xpadneo/issues/295  
我这里通过使能蓝牙 LE Privacy,删除设备并重连后连接成功:  
sudo btmgmt power off  
sudo btmgmt privacy on  
sudo btmgmt power on  

其他配置请详见代码  
## 视频展示
最终效果演示:https://www.bilibili.com/video/BV1aq4y1n7r3?share_source=copy_web  
桌上台架演示:https://www.bilibili.com/video/BV1YM4y157D7?share_source=copy_web
