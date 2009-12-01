
from zope.interface import Interface
from plone.app.portlets.browser.interfaces import IManagePortletsView

class ILayout(Interface):
    """Market interface for layout
    """

class IManageLayoutView(IManagePortletsView):
    """Marker for manage content portlets browser view
    """


MRWIGGIN_CATEGORY = 'mrwiggin'
