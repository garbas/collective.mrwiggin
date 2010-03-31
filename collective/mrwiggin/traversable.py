
from urllib import quote
from Acquisition import aq_acquire
from Acquisition.interfaces import IAcquirer

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from AccessControl.ZopeGuards import guarded_getattr
from Acquisition import Acquired, aq_inner, aq_parent, aq_base
from zExceptions import NotFound
from ZODB.POSException import ConflictError
from OFS.interfaces import ITraversable
import webdav

from zope.interface import implements, Interface
from zope.component import queryMultiAdapter
from zope.traversing.interfaces import TraversalError
from zope.traversing.namespace import nsParse, namespaceLookup

from OFS.Traversable import _marker

def patched_unrestrictedTraverse_plone3(self, path, default=_marker, restricted=False):
    """Lookup an object by path.

    path -- The path to the object. May be a sequence of strings or a slash
    separated string. If the path begins with an empty path element
    (i.e., an empty string or a slash) then the lookup is performed
    from the application root. Otherwise, the lookup is relative to
    self. Two dots (..) as a path element indicates an upward traversal
    to the acquisition parent.

    default -- If provided, this is the value returned if the path cannot
    be traversed for any reason (i.e., no object exists at that path or
    the object is inaccessible).

    restricted -- If false (default) then no security checking is performed.
    If true, then all of the objects along the path are validated with
    the security machinery. Usually invoked using restrictedTraverse().
    """
    if not path:
        return self

    if isinstance(path, str):
        # Unicode paths are not allowed
        path = path.split('/')
    else:
        path = list(path)

    REQUEST = {'TraversalRequestNameStack': path}
    path.reverse()
    path_pop = path.pop

    if len(path) > 1 and not path[0]:
        # Remove trailing slash
        path_pop(0)

    if restricted:
        validate = getSecurityManager().validate

    if not path[-1]:
        # If the path starts with an empty string, go to the root first.
        path_pop()
        obj = self.getPhysicalRoot()
        if restricted:
            validate(None, None, None, obj) # may raise Unauthorized
    else:
        obj = self

    resource = _marker
    try:
        while path:
            name = path_pop()
            __traceback_info__ = path, name

            if name[0] == '_':
                # Never allowed in a URL.
                raise NotFound, name

            if name == '..':
                next = aq_parent(obj)
                if next is not None:
                    if restricted and not validate(obj, obj, name, next):
                        raise Unauthorized(name)
                    obj = next
                    continue

            bobo_traverse = getattr(obj, '__bobo_traverse__', None)
            try:
                if name == 'main_template':
                    raise NotFound(name+', with the BrowserView hook')

                elif name and name[:1] in '@+' and name != '+' and nsParse(name)[1]:
                    # Process URI segment parameters.
                    ns, nm = nsParse(name)
                    try:
                        next = namespaceLookup(
                            ns, nm, obj, self.REQUEST).__of__(obj)
                        if restricted and not validate(
                            obj, obj, name, next):
                            raise Unauthorized(name)
                    except TraversalError:
                        raise AttributeError(name)

                elif bobo_traverse is not None:
                    next = bobo_traverse(REQUEST, name)
                    if restricted:
                        if aq_base(next) is not next:
                            # The object is wrapped, so the acquisition
                            # context is the container.
                            container = aq_parent(aq_inner(next))
                        elif getattr(next, 'im_self', None) is not None:
                            # Bound method, the bound instance
                            # is the container
                            container = next.im_self
                        elif getattr(aq_base(obj), name, _marker) is next:
                            # Unwrapped direct attribute of the object so
                            # object is the container
                            container = obj
                        else:
                            # Can't determine container
                            container = None
                        # If next is a simple unwrapped property, its
                        # parentage is indeterminate, but it may have
                        # been acquired safely. In this case validate
                        # will raise an error, and we can explicitly
                        # check that our value was acquired safely.
                        try:
                            ok = validate(obj, container, name, next)
                        except Unauthorized:
                            ok = False
                        if not ok:
                            if (container is not None or
                                guarded_getattr(obj, name, _marker)
                                    is not next):
                                raise Unauthorized(name)
                else:
                    if getattr(aq_base(obj), name, _marker) is not _marker:
                        if restricted:
                            next = guarded_getattr(obj, name)
                        else:
                            next = getattr(obj, name)
                    else:
                        try:
                            next = obj[name]
                            # The item lookup may return a NullResource,
                            # if this is the case we save it and return it
                            # if all other lookups fail.
                            if isinstance(next,
                                          webdav.NullResource.NullResource):
                                resource = next
                                raise KeyError(name)
                        except AttributeError:
                            # Raise NotFound for easier debugging
                            # instead of AttributeError: __getitem__
                            raise NotFound(name)
                        if restricted and not validate(
                            obj, obj, None, next):
                            raise Unauthorized(name)

            except (AttributeError, NotFound, KeyError), e:
                # Try to look for a view
                next = queryMultiAdapter((obj, self.REQUEST),
                                         Interface, name)

                if next is not None:
                    next = next.__of__(obj)
                    if restricted and not validate(obj, obj, name, next):
                        raise Unauthorized(name)
                elif bobo_traverse is not None:
                    # Attribute lookup should not be done after
                    # __bobo_traverse__:
                    raise e
                else:
                    # No view, try acquired attributes
                    try:
                        if restricted:
                            next = guarded_getattr(obj, name, _marker)
                        else:
                            next = getattr(obj, name, _marker)
                    except AttributeError:
                        raise e
                    if next is _marker:
                        # If we have a NullResource from earlier use it.
                        next = resource
                        if next is _marker:
                            # Nothing found re-raise error
                            raise e

            obj = next

        return obj

    except ConflictError:
        raise
    except:
            if default is not _marker:
                return default
            else:
                raise

def patched_unrestrictedTraverse(self, path, default=_marker, restricted=False):
    """Lookup an object by path.

    path -- The path to the object. May be a sequence of strings or a slash
    separated string. If the path begins with an empty path element
    (i.e., an empty string or a slash) then the lookup is performed
    from the application root. Otherwise, the lookup is relative to
    self. Two dots (..) as a path element indicates an upward traversal
    to the acquisition parent.

    default -- If provided, this is the value returned if the path cannot
    be traversed for any reason (i.e., no object exists at that path or
    the object is inaccessible).

    restricted -- If false (default) then no security checking is performed.
    If true, then all of the objects along the path are validated with
    the security machinery. Usually invoked using restrictedTraverse().
    """
    from webdav.NullResource import NullResource
    if not path:
        return self

    if isinstance(path, str):
        # Unicode paths are not allowed
        path = path.split('/')
    else:
        path = list(path)

    REQUEST = {'TraversalRequestNameStack': path}
    path.reverse()
    path_pop = path.pop

    if len(path) > 1 and not path[0]:
        # Remove trailing slash
        path_pop(0)

    if restricted:
        validate = getSecurityManager().validate

    if not path[-1]:
        # If the path starts with an empty string, go to the root first.
        path_pop()
        obj = self.getPhysicalRoot()
        if restricted:
            validate(None, None, None, obj) # may raise Unauthorized
    else:
        obj = self

    resource = _marker
    try:
        while path:
            name = path_pop()
            __traceback_info__ = path, name

            if name[0] == '_':
                # Never allowed in a URL.
                raise NotFound, name

            if name == '..':
                next = aq_parent(obj)
                if next is not None:
                    if restricted and not validate(obj, obj, name, next):
                        raise Unauthorized(name)
                    obj = next
                    continue

            bobo_traverse = getattr(obj, '__bobo_traverse__', None)
            #if name == 'Members':
            #    import pdb; pdb.set_trace()
            try:
                if name == 'main_template':
                    raise NotFound(name+', with the BrowserView hook')

                elif name and name[:1] in '@+' and name != '+' and nsParse(name)[1]:
                    # Process URI segment parameters.
                    ns, nm = nsParse(name)
                    try:
                        next = namespaceLookup(
                            ns, nm, obj, aq_acquire(self, 'REQUEST'))
                        if IAcquirer.providedBy(next):
                            next = next.__of__(obj)
                        if restricted and not validate(
                            obj, obj, name, next):
                            raise Unauthorized(name)
                    except TraversalError:
                        raise AttributeError(name)

                elif bobo_traverse is not None:
                    next = bobo_traverse(REQUEST, name)
                    if restricted:
                        if aq_base(next) is not next:
                            # The object is wrapped, so the acquisition
                            # context is the container.
                            container = aq_parent(aq_inner(next))
                        elif getattr(next, 'im_self', None) is not None:
                            # Bound method, the bound instance
                            # is the container
                            container = next.im_self
                        elif getattr(aq_base(obj), name, _marker) is next:
                            # Unwrapped direct attribute of the object so
                            # object is the container
                            container = obj
                        else:
                            # Can't determine container
                            container = None
                        # If next is a simple unwrapped property, its
                        # parentage is indeterminate, but it may have
                        # been acquired safely. In this case validate
                        # will raise an error, and we can explicitly
                        # check that our value was acquired safely.
                        try:
                            ok = validate(obj, container, name, next)
                        except Unauthorized:
                            ok = False
                        if not ok:
                            if (container is not None or
                                guarded_getattr(obj, name, _marker)
                                    is not next):
                                raise Unauthorized(name)
                else:
                    if getattr(aq_base(obj), name, _marker) is not _marker:
                        if restricted:
                            next = guarded_getattr(obj, name)
                        else:
                            next = getattr(obj, name)
                    else:
                        try:
                            next = obj[name]
                            # The item lookup may return a NullResource,
                            # if this is the case we save it and return it
                            # if all other lookups fail.
                            if isinstance(next, NullResource):
                                resource = next
                                raise KeyError(name)
                        except AttributeError:
                            # Raise NotFound for easier debugging
                            # instead of AttributeError: __getitem__
                            raise NotFound(name)
                        if restricted and not validate(
                            obj, obj, None, next):
                            raise Unauthorized(name)

            except (AttributeError, NotFound, KeyError), e:
                # Try to look for a view
                next = queryMultiAdapter((obj, aq_acquire(self, 'REQUEST')),
                                         Interface, name)

                if next is not None:
                    if IAcquirer.providedBy(next):
                        next = next.__of__(obj)
                    if restricted and not validate(obj, obj, name, next):
                        raise Unauthorized(name)
                elif bobo_traverse is not None:
                    # Attribute lookup should not be done after
                    # __bobo_traverse__:
                    raise e
                else:
                    # No view, try acquired attributes
                    try:
                        if restricted:
                            next = guarded_getattr(obj, name, _marker)
                        else:
                            next = getattr(obj, name, _marker)
                    except AttributeError:
                        raise e
                    if next is _marker:
                        # If we have a NullResource from earlier use it.
                        next = resource
                        if next is _marker:
                            # Nothing found re-raise error
                            raise e

            obj = next

        return obj

    except ConflictError:
        raise
    except:
        if default is not _marker:
            return default
        else:
            raise
