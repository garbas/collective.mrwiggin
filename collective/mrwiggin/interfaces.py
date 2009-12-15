from zope.interface import Interface
import zope.schema
from zope.schema import Text
from zope.schema import TextLine
from zope.schema import Dict
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.browser.interfaces import IManagePortletsView


class ILayout(Interface):
    """ """

    title = TextLine(title=u"Layout title")
    description = Text(title=u"Layout description")
    icon = TextLine(title=u"Layout icon")
    image = TextLine(title=u"Layout image")

class ILayoutRegistry(Interface):
    """ """

    layouts = Dict(title=u"Layouts list", default=dict())
    assigments = Dict(title=u"Layout assigments", default=dict())


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

