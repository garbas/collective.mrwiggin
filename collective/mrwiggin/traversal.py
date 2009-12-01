
from zope.interface import implements
from zope.component import adapts, getUtility, getMultiAdapter
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces.http import IHTTPRequest

from plone.portlets.interfaces import ILocalPortletAssignable
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping


class MrWigginNamespace(object):

    implements(ITraversable)
    adapts(ILocalPortletAssignable, IHTTPRequest)

    def __init__(self, context, request=None):
        self.context = context
        self.request = request
        
    def traverse(self, name, ignore):
        column = getUtility(IPortletManager, name=name)
        manager = getMultiAdapter((self.context, column), IPortletAssignmentMapping)
        return manager

