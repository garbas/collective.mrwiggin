
from zope.interface import implements, Interface
from zope.component import adapts, getMultiAdapter, queryMultiAdapter
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.portlets.utils import hashPortletInfo
from plone.portlets.interfaces import IPortletRenderer
from plone.app.portlets.browser.editmanager import EditPortletManagerRenderer

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from collective.mrwiggin.interfaces import IManageLayoutView
from collective.mrwiggin.interfaces import IBlockManager
from collective.mrwiggin.interfaces import IRow


class LayoutEditManager(EditPortletManagerRenderer):
    """Render a portlet manager in edit mode for the layout 
    """
    
    adapts(Interface, IDefaultBrowserLayer, IManageLayoutView, IBlockManager)
    template = ViewPageTemplateFile('editmanager.pt')


    def portlets_for_assignments(self, assignments, manager, base_url):
        category = self.__parent__.category
        key = self.__parent__.key
        
        portal = self.context.portal_url.getPortalObject()
        view = portal.restrictedTraverse('@@plone')
        
        data = []
        for idx in range(len(assignments)):
            name = assignments[idx].__name__
            
            editview = queryMultiAdapter(
                (assignments[idx], self.request), name='edit', default=None)
            
            if editview is None:
                editviewName = ''
            else:
                editviewName = '%s/%s/edit' % (base_url, name)
            
            portlet_hash = hashPortletInfo(
                dict(manager=manager.__name__, category=category,
                     key=key, name=name,))
            
            renderer = getMultiAdapter(
                        (self.context, self.request, view,
                            manager, assignments[idx]),
                                IPortletRenderer)

            data.append({
                'title'      : assignments[idx].title,
                'editview'   : editviewName,
                'hash'       : portlet_hash,
                'renderer'   : renderer.__of__(self.context),
                'up_url'     : '%s/@@move-portlet-up?name=%s' % (base_url, name),
                'down_url'   : '%s/@@move-portlet-down?name=%s' % (base_url, name),
                'delete_url' : '%s/@@delete-portlet?name=%s' % (base_url, name),
                })
        if len(data) > 0:
            data[0]['up_url'] = data[-1]['down_url'] = None
            
        return data
    
    def safe_render(self, portlet_renderer):
        try:
            return portlet_renderer.render()
        except ConflictError:
            raise
        except Exception:
            log.exception('Error while rendering %r' % (self,))
            aq_acquire(self, 'error_log').raising(sys.exc_info())
            return self.error_message()


class RowEditManager(LayoutEditManager):
    """Render a portlet manager in edit mode for the rows 
    """
    
    adapts(Interface, IDefaultBrowserLayer, IManageLayoutView, IRow)
    template = ViewPageTemplateFile('editmanager_row.pt')


