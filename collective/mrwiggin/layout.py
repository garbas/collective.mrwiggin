
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
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from collective.mrwiggin.interfaces import MRWIGGIN_CATEGORY
from collective.mrwiggin.interfaces import IManageLayoutView
from collective.mrwiggin.interfaces import ILayout



class MainLayout(BrowserView):
    """Main layout
    """

    implements(ILayout)


