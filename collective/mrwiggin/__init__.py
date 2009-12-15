from zope.i18nmessageid import MessageFactory
MessageFactory = MessageFactory('collective.mrwiggin')

from collective.mrwiggin.interfaces import ILayout
from collective.mrwiggin.interfaces import ILayoutRegistry

class registry(ILayoutRegistry):
    pass

class mainlayout(ILayout):
    pass

