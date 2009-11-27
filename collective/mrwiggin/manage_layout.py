
from zope.interface import implements
from zope.interface import Interface
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.browser.editmanager import EditPortletManagerRenderer
from plone.app.portlets.manager import DashboardPortletManagerRenderer
from plone.app.portlets.interfaces import IColumn

from Products.Five import BrowserView

from collective.mrwiggin.interfaces import MRWIGGIN_CATEGORY
from collective.mrwiggin.interfaces import IManageLayoutView


class ManageLayout(BrowserView):
    """
    """

    implements(IManageLayoutView)
    
    def __init__(self, context, request):
        super(ManageLayout, self).__init__(context, request)
        
    # IManagePortletsView implementation

    @property
    def macros(self):
        return self.index.macros
    
    @property
    def category(self):
        return MRWIGGIN_CATEGORY
        
    @property
    def key(self):
        return ('/'.join(self.context.getPhysicalPath()))
    
    def getAssignmentMappingUrl(self, manager):
        baseUrl = str(getMultiAdapter((self.context, self.request), name='absolute_url'))
        return '%s/++block++%s' % (baseUrl, manager.__name__)
    
    def getAssignmentsForManager(self, manager):
        assignments = getMultiAdapter((self.context, manager), IPortletAssignmentMapping)
        return assignments.values()

    def layout_id(self):
        custom_layout = self.request.get('layout', None)
        if custom_layout:
            return custom_layout
        _context = self.context.get(self.context.getDefaultPage(), self.context)
        return _context.getLayout()

    def is_layout(self):
        # TODO: check if layout exists
        return True

    def layout(self):
        view = self.context.restrictedTraverse('@@'+self.layout_id())
        self.template = view.template
        return view.main_template.macros['body']

class LayoutEditManager(EditPortletManagerRenderer):
    """Render a portlet manager in edit mode for the dashboard
    """
    adapts(Interface, IDefaultBrowserLayer, IManageLayoutView, IPortletManager)


