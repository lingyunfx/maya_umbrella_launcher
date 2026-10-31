## maya-umbrella-launcher

一个基于[maya-umbrella](https://github.com/loonghao/maya_umbrella)的Maya桌面启动器，使用 uv 管理 Python 3.10 环境（Windows x64）。


## 功能
 - 拥有图形界面和命令行两种模式
 - 启动Maya并自动配置maya-umbrella环境
 - 可不依赖于启动器，进行本地安装
 - 检查更新功能
 - 双语支持

## 使用说明

### 图像界面
从 release 下载 `MayaUmbrellaLauncher-版本号-Setup.exe` 安装包，安装后通过开始菜单启动。
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

## 开发运行

安装 [uv](https://docs.astral.sh/uv/getting-started/installation/) 后，在项目根目录执行：

```powershell
uv run start
uv run launcher_cmd --help
```

uv 会自动下载 Python 3.10、创建 `.venv` 并按 `uv.lock` 同步依赖，无需手动激活环境。
原生 uv 不支持给不带参数的 `uv run` 配置默认命令，请使用 `uv run start`。
也可使用 `uv run python -m maya_umbrella_launcher`。
界面使用 PySide6 / Qt 6 与 dayu-widgets 1.1.1；开发环境固定为 Python 3.10，由 uv 自动管理。

## 编译和安装包

在 Windows x64 安装 [Inno Setup 6 或 7](https://jrsoftware.org/isdl.php)，然后执行：

```powershell
uv run build
```

该命令先使用 Nuitka 编译图形和命令行程序，再使用 Inno Setup 生成安装包：
`dist/MayaUmbrellaLauncher-0.1.3-Setup.exe`。
首次构建需要网络；Nuitka 使用已有 MSVC，未找到时会下载所需编译工具。
自定义 Inno Setup 路径可设置 `$env:ISCC = 'D:\Inno Setup 6\ISCC.exe'`。
编译中间产物位于 `build/`。任一步失败都会停止，不会报告构建成功。

安装包按当前用户安装，无需管理员权限，包含 Python、Qt、界面资源和卸载功能。
命令行程序安装在 `cli/launcher_cmd.exe`，图形程序位于安装目录根目录。
安装包未签名。发布前可对可执行文件与安装包进行代码签名。

## 检查

```powershell
uv run python -m unittest discover -s tests
```
