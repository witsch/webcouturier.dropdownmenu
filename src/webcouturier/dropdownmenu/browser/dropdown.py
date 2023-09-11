# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from Acquisition import aq_inner
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.viewlets import common
from plone.app.portlets.portlets.navigation import Assignment
from plone.memoize.compress import xhtml_compress
from plone.memoize.ram import cache
from Products.CMFCore.interfaces import IContentish
from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from webcouturier.dropdownmenu.browser.interfaces import IDropdownConfiguration
from webcouturier.dropdownmenu.browser.interfaces import IDropdownMenuViewlet
from zope.component import getMultiAdapter
from zope.interface import implementer

import plone.api


def _get_cfg(name):
    return plone.api.portal.get_registry_record(
        name,
        interface=IDropdownConfiguration
    )


class DropdownQueryBuilder(NavtreeQueryBuilder):
    """Build a folder tree query suitable for a dropdownmenu
    """

    def __init__(self, context):
        NavtreeQueryBuilder.__init__(self, context)
        self.query['path'] = {
            'query': '/'.join(context.getPhysicalPath()),
            'navtree_start': 1,
            'depth': _get_cfg('dropdown_depth')
        }


@implementer(IDropdownMenuViewlet)
class DropdownMenuViewlet(common.GlobalSectionsViewlet):
    """A custom version of the global navigation class that has to have
       dropdown menus for global navigation tabs objects
    """

    #
    # Define a cache key: every instance (probabily only one per site,
    # language and user gets its/his own cache so we don't get the
    # menu retrieved in the wrong language nor conflicts due to view
    # permissions. (A manager might be able to view more pages than an
    # anonymous user.)
    #
    def _render_cachekey(fun, self):
        return ''.join((
            self.selected_portal_tab,
            plone.api.portal.get_current_language(aq_inner(self.context)),
            str(plone.api.user.is_anonymous()),
        ))

    # Cache by

    # ---> Viewlet Name -> should be always identical since no one
    #                      will use two drop down menus, won't he?
    # ---> Selected/Higlighted Tab -> solved current problem
    # ---> By language -> expect to be fixed, if we cache by user
    # ---> User Name -> this is the worst part however if there are
    #                   many logged in users

    #
    # Summary: every user and every visited section gets its own
    # instance in the ram.cache.
    #
    # Suggestion: we should improve this in a manner that not every
    # user needs its own set of instances in the cache
    #
    # If we can't solve this issue caching won't make much use but
    # consume lots of ram.
    #
    # :-(

    #
    # Original template goes here
    #
    _template = ViewPageTemplateFile('dropdown_sections.pt')

    #
    # use cache decoration in order to store/retrieve function output
    # to/from cache
    @cache(_render_cachekey)
    def cached_viewlet(self):
        return xhtml_compress(self._template())

    def index(self):
        if self.enable_caching:
            return self.cached_viewlet()
        else:
            return self._template()

    recurse = ViewPageTemplateFile('dropdown_recurse.pt')

    @property
    def enable_caching(self):
        return _get_cfg('enable_caching')

    @property
    def enable_parent_clickable(self):
        return _get_cfg('enable_parent_clickable')

    @property
    def enableImages(self):
        return _get_cfg('enable_images')

    @property
    def imgSize(self):
        return _get_cfg('img_size')

    @property
    def enableDesc(self):
        return _get_cfg('enable_desc')

    def update(self):
        common.ViewletBase.update(self)  # Get portal_state and portal_url
        super(DropdownMenuViewlet, self).update()
        context = aq_inner(self.context)
        portal_props = plone.api.portal.get_tool('portal_properties')
        self.properties = portal_props.navtree_properties
        self.navroot_path = getNavigationRoot(context)
        self.navroot_path = getNavigationRoot(context)
        try:
            if IContentish.providedBy(context):
                uid = plone.api.content.get_uuid(obj=context)
            else:
                uid = None
        except TypeError:
            # ArcheTypes (such as PFG FormFolder) have no UID yet when the
            # factory gets called.
            uid = None
        self.data = Assignment(root_uid=uid)

    def getTabObject(self, tabUrl='', tabPath=None):
        if tabUrl == self.portal_state.navigation_root_url():
            # We are at the navigation root
            return ''
        if tabPath is None:
            # get path for current tab's object
            try:
                # we are in Plone > 3.0.x
                tabPath = tabUrl.split(self.site_url)[-1]
            except AttributeError:
                # we are in Plone 3.0.x world
                tabPath = tabUrl.split(self.portal_url)[-1]

            if tabPath == '' or '/view' in tabPath:
                # It's either the 'Home' or Image tab. It can't have
                # any dropdown.
                return ''

            if tabPath.startswith('/'):
                tabPath = tabPath[1:]
            elif tabPath.endswith('/'):
                # we need a real path, without a slash that might appear
                # at the end of the path occasionally
                tabPath = str(tabPath.split('/')[0])

            if '%20' in tabPath:
                # we have the space in object's ID that has to be
                # converted to the real spaces
                tabPath = tabPath.replace('%20', ' ').strip()

        if tabPath == '':
            return ''

        portal = self.portal_state.portal()
        portal_path = '/'.join(portal.getPhysicalPath())
        # Check to see if we are using a navigation root. If we are
        # virtual hosting the navigation root as its own domain,
        # the tabPath is no longer rooted at the main portal.
        try:
            if portal_path != self.navroot_path:
                portal = portal.restrictedTraverse(self.navroot_path)
            tabObj = portal.restrictedTraverse(tabPath, None)
        except Unauthorized:
            # Unauthorized can happen when error page is rendered in
            # unallowed context
            return ''

        if tabObj is None:
            # just in case we have missed any possible path
            # in conditions above
            return ''

        strategy = getMultiAdapter((tabObj, self.data), INavtreeStrategy)
        queryBuilder = DropdownQueryBuilder(tabObj)
        query = queryBuilder()

        data = buildFolderTree(tabObj, obj=tabObj, query=query,
                               strategy=strategy)

        bottomLevel = self.data.bottomLevel or self.properties.getProperty(
            'bottomLevel', 0)

        def flatten(items, level=0):
            if bottomLevel <= 0 or level <= bottomLevel:
                for item in items:
                    yield dict(item, level=level)
                    if item.get('show_children'):
                        children = item.get('children', [])
                        for child in flatten(children, level=level+1):
                            yield child

        def add_last(items):
            last = 0
            for item in items:
                yield dict(item, last=last)
                last = item['level']

        children = list(add_last(flatten(data.get('children', []))))
        return self.recurse(children=children).strip()
