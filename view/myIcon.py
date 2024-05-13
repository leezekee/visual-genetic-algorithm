from enum import Enum

from qfluentwidgets import Theme, FluentIconBase


class MyIcon(FluentIconBase, Enum):
    """ Custom icons """

    GRAPH = "graph"
    CHART = "chart"
    DATA = "data"
    ADD_NODE = "addNode"
    ADD_EDGE = "addEdge"
    REMOVE_NODE = "removeNode"
    REMOVE_EDGE = "removeEdge"
    NORMAL = "normal"
    START = "start"
    STOP = "stop"
    CLEAR = "clear"
    SAVE = "save"
    LOAD = "load"
    GA = "ga"
    ALGORITHM = "algorithm"
    CONFIRM = "confirm"
    GO = "go"

    def path(self, theme=Theme.AUTO):
        # getIconColor() 根据主题返回字符串 "white" 或者 "black"
        return f'assets/{self.value}.png'
