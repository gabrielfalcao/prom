# -*- coding: utf-8 -*-


class Node(object):
    DEFAULT_IDENTITY_KEY = "title"

    def __init__(self, __parent__=None, __children__=None, **data):
        self.__parent__ = __parent__
        self.__children__ = __children__
        self.__data__ = data

    def identity(self):
        return self.__data__.get(self.DEFAULT_IDENTITY_KEY)

    def to_string(self):
        return json.dumps(self.to_dict())

    def __unicode__(self):
        return self.to_string().encode("utf8")

    def to_dict(self):
        return dict(
            filter(
                lambda k, v: bool(v),
                {
                    "data": self.__data__.copy(),
                    "children": self.__children__,
                    "parent": self.__parent__,
                }.items(),
            )
        )

    def get_children(self):
        return self.__children__

    def get_data(self):
        return self.__data__

    def get_parent(self):
        return self.__parent__


class TodoGroup(Node):
    def get_children(self):
        if not self.__children__:
            return ()

        return tuple(self.__children__)


class TodoItem(Node):
    def get_children(self):
        return None
