from zope.interface import implements
from zope.component import getUtility, getMultiAdapter

from Acquisition import aq_inner

from plone.app.kss.interfaces import IPloneKSSView
from plone.app.kss.plonekssview import PloneKSSView as base

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletManagerRenderer
from plone.app.portlets.browser.kss import PortletManagerKSS as BasePortletManagerKSS 


class PortletManagerKSS(BasePortletManagerKSS):

    def _render_column(self, info, view_name):
        ksscore = self.getCommandSet('core')

        context = aq_inner(self.context)
        request = aq_inner(self.request)
        view = getMultiAdapter((context, request), name=view_name)
        manager = getUtility(IPortletManager, name=info['manager'])

        request['key'] = info['key']

        request['viewname'] = view_name
        renderer = getMultiAdapter((context, request, view, manager,), IPortletManagerRenderer)
        renderer.update()
        renderer_html = renderer.__of__(context).render()
        split_string = '<!-- split point (i know its dumbt to do like this) -->'

        ksscore.replaceInnerHTML(
            ksscore.getCssSelector('div#portletmanager-renderer-' + info['manager'].replace('.', '-')),
            renderer_html.split(split_string)[1])
        ksscore.replaceInnerHTML(
            ksscore.getCssSelector('div#portletmanager-' + info['manager'].replace('.', '-') + ' .portletAssignmentsList'),
            renderer_html.split(split_string)[3])

        return self.render()
