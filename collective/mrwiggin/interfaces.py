
from zope.interface import Interface
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.browser.interfaces import IManagePortletsView


class ILayout(Interface):
    """Market interface for layout
    """

class IManageLayoutView(IManagePortletsView):
    """Marker for manage content portlets browser view
    """

class IBlockManager(IPortletManager):
    """Common base class for mrwiggin layout portlets.
    """

class IRow(IBlockManager):
    """Common base class for row portlets.
    """

class IColumn(IBlockManager):
    """Common base class for column portlets.
    """


MRWIGGIN_CATEGORY = 'mrwiggin'
