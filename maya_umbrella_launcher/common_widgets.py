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
