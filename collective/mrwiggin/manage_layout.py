
from zope.interface import implements
from zope.component import getMultiAdapter

from plone.memoize.instance import memoize
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.app.portlets.browser.manage import ManageContextualPortlets

from collective.mrwiggin.interfaces import IManageLayoutView
from collective.mrwiggin.interfaces import ILayout


class ManageLayout(ManageContextualPortlets):
    implements(IManageLayoutView)
   
    def __init__(self, context, request):
        super(ManageLayout, self).__init__(context, request)
        self.request.set('disable_border', False)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        self.site_url = portal_state.portal_url()

    @property
    def category(self):
        return CONTEXT_CATEGORY
        
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

    @memoize
    def layout(self):
        return self.context.restrictedTraverse('@@'+self.layout_id())

    def portal_layout(self):
        return self.layout().index.macros['portal-layout']

