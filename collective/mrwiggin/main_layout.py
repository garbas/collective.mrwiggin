
import os.path

from zope.component import queryUtility, getMultiAdapter
from plone.registry.interfaces import IRegistry

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MainLayout(BrowserView):

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)

        registry = queryUtility(IRegistry)
        if registry:
            layout_name = self.request.get('mrwiggin_layout', None)
            assigments = registry.records.get('collective.mrwiggin.assigments', None)
            if layout_name is None and assigments:
                # search in registry for
                # please excuse my magic :P
                # from /a/b/c creates ['/a/b/c', '/a/b', '/a']
                # and then check for each record in registry
                portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
                t = self.context.absolute_url()[len(portal_state.portal_url()):].split('/')
                for path in reversed(
                        ['/'+os.path.join(*[str(t[j])
                                for j in range(t.index(i)+1)])
                                        for i in t]):
                    layout_name = assigments.value.get(path, None)
                    if layout_name is not None:
                        break

            layouts = registry.records.get('collective.mrwiggin.layouts', None)
            if layouts is not None and \
               layout_name is not None and \
               layout_name in layouts.value.keys():
                self.index = ViewPageTemplateFile(
                        self.resolve_layout_path(
                                layouts.value[layout_name]))


    def resolve_layout_path(self, name):
        module, path = name.split(':')
        return os.path.join(*(
                    [os.path.dirname(
                        __import__(module, globals(), locals(), ['']).__file__),] + \
                            path.split('/')))
