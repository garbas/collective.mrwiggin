
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.browser.interfaces import IManagePortletsView


class IContentPortlets(IPortletManager):
    """Common base class for content portlets columns.
    
    Register a portlet for IContentPortlets if it is applicable to regular columns
    but not to others .
    """

class IManageLayoutView(IManagePortletsView):
    """Marker for manage content portlets browser view
    """




MRWIGGIN_CATEGORY = 'mrwiggin'
