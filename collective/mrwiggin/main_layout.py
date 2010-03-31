
import os.path

from zope.interface import alsoProvides, implements
from zope.component import queryUtility, getMultiAdapter
from plone.registry.interfaces import IRegistry

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MainLayout(BrowserView):
    
    def get_viewtemplate(self):
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
                tt = ['/'+os.path.join(*[str(t[j]) for j in range(t.index(i)+1)]) for i in t]
                for path in reversed(tt):
                    layout_name = assigments.value.get(path, None)
                    if layout_name is not None:
                        break

            layouts = registry.records.get('collective.mrwiggin.layouts', None)
            if layouts is not None and \
               layout_name is not None and \
               layout_name in layouts.value.keys():
                layout_path = self.resolve_layout_path(layouts.value[layout_name])
                return ViewPageTemplateFile(layout_path)
        return ViewPageTemplateFile(
                        self.resolve_layout_path(
                                'Products.CMFPlone:skins/plone_templates/main_template.pt'))
    
    @property
    def index(self):
        self.get_viewtemplate()(self)
    
    @property
    def macros(self):
        return self.get_viewtemplate().macros

    def resolve_layout_path(self, name):
        module, path = name.split(':')
        return os.path.join(*(
                    [os.path.dirname(
                        __import__(module, globals(), locals(), ['']).__file__),] + \
                            path.split('/')))

