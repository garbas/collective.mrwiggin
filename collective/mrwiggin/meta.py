
import os
import zope.schema
import zope.interface
import zope.configuration
import zope.component.zcml

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.app.publisher.browser.menumeta import menuItemDirective as browser_menuItem
from Products.Five.browser.metaconfigure import page as browser_page

from collective.mrwiggin import MessageFactory as _


class ILayout(zope.interface.Interface):
    """Directive which registers a new layout."""

    name = schema.TextLine(
        title           = _(u"Name"),
        description     = _(u"A unique name for the layout."),
        required        = True,
        )
   
    class_ = configuration_fields.GlobalObject(
        title           = _("Class"),
        description     = _("A class acting as the renderer."),
        required        = True,
        )
    
    for_ = zope.configuration.fields.GlobalObject(
        title           = _("Context object type for which this layout is used"),
        description     = _("""An interface or class"""),
        default         = zope.interface.Interface,
        required        = False,
        )
    layer = zope.configuration.fields.GlobalObject(
        title           = _("Browser layer for which this layout is used"),
        description     = _("""An interface or class"""),
        default         = IDefaultBrowserLayer,
        required        = False,
        )

    permission = zope.schema.TextLine(
        title           = _(u"View permission"),
        description     = _(u"Permission used for viewing the layout."),
        default         = u"zope2.View",
        required        = False,
        )

    title = zope.configuration.fields.MessageID(
        title           = _(u"Title"),
        description     = _(u"The text to be displayed for the menu item"),
        default         = None,
        required        = False,
        )

    description = zope.configuration.fields.MessageID(
        title           = _(u"A longer explanation of the menu item"),
        description     = _(u"""A UI may display this with the item or display it when the
                              user requests more assistance."""),
        default         = u'',
        required        = False,
        )

    icon = zope.schema.TextLine(
        title           = _(u"Icon Path"),
        description     = _(u"Path to the icon resource representing this menu item."),
        default         = None,
        required        = False,
        )


def LayoutDirective(_context, name, class_,
                        for_ = zope.interface.Interface,
                        layer = IDefaultBrowserLayer,
                        permission = u"zope2.View",
                        title = None,
                        description = u'',
                        icon = None):

    # calculate defualt values
    title = title and title or class_.getattr('title', unicode(name))
    description = description and description or class_.getattr('description', u'')
    icon = icon and icon or class_.getattr('icon', None)

    # register browser:page
    browser_page(_context, name, permission, for_,
        layer=layer, title=title, class_=XXX)

    # register browser:menuItem
    browser_menuItem(_context, 'plone_displayviews', for_, '@@'+name, title,
        description=description, icon=icon, permission=permission, layer=layer)



