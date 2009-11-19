
from zope.interface import implements
from zope.component import getMultiAdapter

from Products.Five import BrowserView
from plone.portlets.interfaces import IPortletAssignmentMapping

from collective.mrwiggin.interfaces import MRWIGGIN_CATEGORY
from collective.mrwiggin.interfaces import IManageLayoutView


class ManageLayout(BrowserView):
    """
    """

    implements(IManageLayoutView)
    
    def __init__(self, context, request):
        super(ManageContentPortlets, self).__init__(context, request)
        self.request.set('disable_border', True)
        
    # IManagePortletsView implementation

    @property
    def macros(self):
        return self.index.macros
    
    @property
    def category(self):
        return MRWIGGIN_CATEGORY
        
    @property
    def key(self):
        return ('/'.join(self.context.getPhysicalPath()))+self.display()
    
    def getAssignmentMappingUrl(self, manager):
        baseUrl = str(getMultiAdapter((self.context, self.request), name='absolute_url'))
        return '%s/++block++%s' % (baseUrl, manager.__name__)
        #return '%s/++block++%s+%s' % (baseUrl, manager.__name__, layoutId)
    
    def getAssignmentsForManager(self, manager):
        # TODO: look into what this does
        assignments = getMultiAdapter((self.context, manager), IPortletAssignmentMapping)
        return assignments.values()

    def display(self):
        _context = self.context.get(self.context.getDefaultPage(), self.context)
        return _context.getLayout()


