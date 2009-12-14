
import os

from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.mrwiggin.interfaces import ILayout


class IMainLayout(ILayout):
    pass


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
                t = path_as_dict
                for path in reversed(
                        ['/'+os.path.join(*[str(t[j])
                                for j in range(t.index(i)+1)])
                                        for i in t]):
                    layout_name = assigments.get(path, None)
                    if layout_name is not None:
                        break

            layouts = registry.records.get('collective.mrwiggin.layouts', dict())
            if layout_name is not None and \
               layout_name in layouts.keys():
                self.index = ViewPageTemplateFile(
                        self.resolve_layout_path(
                                layouts[layout_name]))


    # FIXME: we need to cache this on 
    def resolve_layout_path(self, name):
        module, path = name.split(':')
        return os.path.join(*(
                    [os.path.dirname(__import__(module).__file__),] + \
                            path.split('/')))
