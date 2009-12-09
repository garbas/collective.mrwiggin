
from zope.interface import implements
from zope.component import getMultiAdapter

from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.constants import CONTEXT_CATEGORY

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from collective.mrwiggin.interfaces import IManageLayoutView
from collective.mrwiggin.interfaces import ILayout


class ManageLayout(BrowserView):
    """
    """

    implements(IManageLayoutView)
   
    def __init__(self, context, request):
        super(ManageLayout, self).__init__(context, request)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        self.site_url = portal_state.portal_url()

    # IManagePortletsView implementation

    @property
    def macros(self):
        return self.index.macros
    
    @property
    def category(self):
        return CONTEXT_CATEGORY
        
    @property
    def key(self):
        return ('/'.join(self.context.getPhysicalPath()))
    
    def getAssignmentMappingUrl(self, manager):
        baseUrl = str(getMultiAdapter((self.context, self.request), name='absolute_url'))
        return '%s/++mrwiggin++%s' % (baseUrl, manager.__name__)
    
    def getAssignmentsForManager(self, manager):
        assignments = getMultiAdapter((self.context, manager), IPortletAssignmentMapping)
        return assignments.values()

    # IManageLayoutView implementation

    @memoize
    def layout_id(self):
        custom_layout = self.request.get('layout', None)
        if custom_layout:
            return custom_layout

        _context = self.context

        default_page = self.context.getDefaultPage()
        if default_page:
            _context = self.context.get(default_page)
        
        return _context.getLayout()

    @memoize
    def is_layout(self):
	return ILayout.providedBy(self.layout())

    #@memoize
    def layout(self):
        return self.context.restrictedTraverse('@@'+self.layout_id())

    def portal_layout(self):
        return self.layout().index.macros['portal-layout']

