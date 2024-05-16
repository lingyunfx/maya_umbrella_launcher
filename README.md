## maya-umbrella-launcher

一个基于[maya-umbrella](https://github.com/loonghao/maya_umbrella)的Maya桌面启动器，使用Python3.9。  


## Features
 - 拥有图形界面和命令行两种模式
 - 启动Maya并自动配置maya-umbrella环境
 - 可不依赖于启动器，进行本地安装
 - 自动更新功能
 - 双语支持

## Usage
从release下载最新版本，解压后运行`maya_umbrela_launcher.exe`即可。
打开后界面长这样:

![](https://lingyunfx-1259219315.cos.ap-beijing.myqcloud.com/pic/20240516235008.png)

> 1.首先需要设置插件存放的路径，点击设置按钮打开面板  

![](https://lingyunfx-1259219315.cos.ap-beijing.myqcloud.com/pic/20240516235150.png)

> 2.选择一个目录，然后点击下载

![](https://lingyunfx-1259219315.cos.ap-beijing.myqcloud.com/pic/20240516235311.png)

> 下载完成后，关闭设置面板，点击启动按钮即可启动Maya  
> 开启maya可以看到插件加载成功的提示

![](https://lingyunfx-1259219315.cos.ap-beijing.myqcloud.com/pic/20240517000016.png)

## Third-party libraries used
 - PySide2
 - dayu_widgets
 - requests

 `pip install -r requirements.txt`
 
## 打包
```shell
pyinstaller -i resource/app_umbrella.ico view.py --onefile
```