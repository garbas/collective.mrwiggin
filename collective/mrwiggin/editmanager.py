
from zope.interface import Interface
from zope.component import adapts
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.browser.interfaces import IManageContextualPortletsView
from plone.app.portlets.browser.editmanager import ContextualEditPortletManagerRenderer
from plone.app.portlets.manager import ColumnPortletManagerRenderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.mrwiggin.interfaces import IMrWigginLayer


class LayoutEditPortletManager(ContextualEditPortletManagerRenderer, ColumnPortletManagerRenderer):
    """Render a portlet manager in edit mode for the layout 
    """
    
    adapts(Interface, IMrWigginLayer, IManageContextualPortletsView, IPortletManager)
    template = ViewPageTemplateFile('editmanager.pt')

