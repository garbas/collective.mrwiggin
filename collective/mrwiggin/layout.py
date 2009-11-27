
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class BaseLayout(BrowserView):
   
    template = None
    main_template = ViewPageTemplateFile('layout.pt')

    def __call__(self, *args, **kw):
        return self.main_template(self, *args, **kw)

    def body_macro(self):
        pass
