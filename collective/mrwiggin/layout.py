
from Products.Five import BrowserView
from collective.mrwiggin.interfaces import ILayout


class Layout(BrowserView):
    implements(ILayout)


