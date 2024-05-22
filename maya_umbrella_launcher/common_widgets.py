import dayu_widgets as dy
from PySide2 import QtWidgets, QtCore


class WidgetMixin(object):

    def __init__(self):
        self.main_layout = QtWidgets.QVBoxLayout()

    def add_widgets_v_line(self, *args, side=None, stretch=False):
        return self.__add_widgets(*args, side=side, stretch=stretch, layout_func=QtWidgets.QVBoxLayout)

    def add_widgets_h_line(self, *args, side=None, stretch=False):
        return self.__add_widgets(*args, side=side, stretch=stretch, layout_func=QtWidgets.QHBoxLayout)

    def __add_widgets(self, *args, side=None, stretch=False, layout_func=None):
        layout = layout_func()

        side_dict = {'right': QtCore.Qt.AlignRight,
                     'left': QtCore.Qt.AlignLeft,
                     'top': QtCore.Qt.AlignTop,
                     'center': QtCore.Qt.AlignCenter
                     }
        if side:
            layout.setAlignment(side_dict.get(side, QtCore.Qt.AlignTop))

        for item in args:
            if isinstance(item, QtWidgets.QLayout):
                layout.addLayout(item)
            elif isinstance(item, QtWidgets.QWidget):
                layout.addWidget(item)

        if stretch:
            layout.addStretch(stretch)

        self.main_layout.addLayout(layout)

        return layout


class CommonDialog(QtWidgets.QDialog, WidgetMixin):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        WidgetMixin.__init__(self)


class CommonWidget(QtWidgets.QWidget, WidgetMixin):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        WidgetMixin.__init__(self)


def question_box(text, parent=None):
    answer = QtWidgets.QMessageBox.question(parent,
                                            'Confirm?',
                                            text,
                                            QtWidgets.QMessageBox.Yes |
                                            QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No,
                                            )
    if answer != QtWidgets.QMessageBox.Yes:
        return False
    return True


def show_message(text, duration=3.0, typ='info', pos_center=False, parent=None):
    """
    显示dy.MMessage消息框
    Args:
        text(unicode): 显示的消息文字
        duration(float): 显示消息的持续时间，单位为秒
        typ(str): 显示的消息框类型，支持参数有 info, success, warning, error
        pos_center(bool): 是否显示在屏幕中央
        parent(QObject): 父级
    """
    if pos_center:
        msg = getattr(dy.MToast, typ)(text=text, duration=duration, parent=parent)
    else:
        msg = getattr(dy.MMessage, typ)(text=text, duration=duration, parent=parent)
    msg.show()
