
from zope.interface import Interface
from zope.schema import Dict
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.browser.interfaces import IManagePortletsView


class ILayout(Interface):
    """ """

    title = TextLine(title=u"Layout title")
    description = Text(title=u"Layout description")
    template = TextLine(title=u"Layout template")


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

