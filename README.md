## maya-umbrella-launcher

一个基于[maya-umbrella](https://github.com/loonghao/maya_umbrella)的Maya桌面启动器，使用Python3.9。  


## 功能
 - 拥有图形界面和命令行两种模式
 - 启动Maya并自动配置maya-umbrella环境
 - 可不依赖于启动器，进行本地安装
 - 检查更新功能
 - 双语支持

## 使用说明

### 图像界面
从release下载最新版本，解压后运行`maya_umbrela_launcher.exe`即可。
打开后界面长这样:

<img src="https://lingyunfx-1259219315.cos.ap-beijing.myqcloud.com/pic/20240516235008.png" width="70%" height="70%">


> 1.首先需要设置插件存放的路径，点击设置按钮打开面板  

<img src="https://lingyunfx-1259219315.cos.ap-beijing.myqcloud.com/pic/20240516235150.png" width="70%" height="70%">


> 2.选择一个目录，然后点击下载
 
<img src="https://lingyunfx-1259219315.cos.ap-beijing.myqcloud.com/pic/20240516235311.png" width="70%" height="70%">

> 下载完成后，关闭设置面板，点击启动按钮即可启动Maya  
> 开启maya可以看到插件加载成功的提示

<img src="https://lingyunfx-1259219315.cos.ap-beijing.myqcloud.com/pic/20240517000016.png" width="70%" height="70%">

### 命令行模式

打开cmd窗口，使用`cd`命令切换到`launcher_cmd.exe`所在的文件夹。

```shell
# 查看帮助说明
launcher_cmd.exe -h
```

1.指定插件目录
```shell
launcher_cmd.exe - p <插件目录>
```

2.下载插件
```shell
launcher_cmd.exe -d
````

3.打开maya软件
```shell
# 参数为maya版本号
launcher_cmd.exe -s 2018
```

4.也可以进行本地安装
```shell
launcher_cmd.exe -i 2018
```

卸载:
```shell
launcher_cmd.exe -u 2018
```

## 第三方库
 - PySide2
 - dayu_widgets
 - requests

 `pip install -r requirements.txt`
 
## 打包
```shell
pyinstaller -i resource/app_umbrella.ico view.py --onefile -p .
```
