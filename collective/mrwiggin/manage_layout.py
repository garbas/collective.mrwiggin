
from zope.interface import implements
from plone.app.portlets.browser.manage import ManageContextualPortlets
from collective.mrwiggin.interfaces import IManageLayoutView
from collective.mrwiggin.main_layout import MainLayout


class ManageLayout(MainLayout, ManageContextualPortlets):
    implements(IManageLayoutView)
    
    def __call__(self):
        return self.index.__of__(self)()

    def is_manage_layout(self):
        return True

    def language(self):
        pass        
