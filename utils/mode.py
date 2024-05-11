from enum import Enum


class Mode(Enum):
	''' 模式 '''
	NORMAL = "Normal"
	ADD_NODE = "Add Node"
	ADD_EDGE = "Add Edge"
	REMOVE_NODE = "Remove Node"
	REMOVE_EDGE = "Remove Edge"
