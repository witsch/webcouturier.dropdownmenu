# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'webcouturier.dropdownmenu:uninstall',
            'webcouturier.dropdownmenu:create_content',
        ]


def create_content(context):
    """Create Content for tests and development."""
    portal = api.portal.get()

    def _make_folders(container,
                      max_items,
                      max_depth,
                      depth=0,
                      base_number=u''):
        """local method to recursive create content."""

        if depth >= max_depth:
            return

        for i in range(1, max_items+1):
            number = u'{0}{1}'.format(base_number, i)
            # folder = u'{0}Folder {1}'.format('Sub '*depth, number)
            folder = api.content.create(
                container=container,
                type='Folder',
                title=u'{0}Folder {1}'.format('Sub '*depth, number),
            )
            api.content.transition(folder, transition='publish')
            number = u'{0}{1}'.format(number, u'.')
            _make_folders(
                container=folder,
                max_items=max_items,
                max_depth=max_depth,
                depth=depth+1,
                base_number=number,
            )

    # creating lots of folders. 5 per level, 4 levels deep. 780 pcs!
    _make_folders(
        container=portal,
        max_items=5,
        max_depth=4,
    )

    # now lets reduce the amount to get different appearances.
    remove_folders = []

    # remove all sub items from the first sub folder.
    remove_folders.extend(
        [i[1] for i in portal.
         get('folder-1').
         get('sub-folder-1.1').
         contentItems()],
    )

    # remove all sub items from the first sub sub folder.
    remove_folders.extend(
        [i[1] for i in portal.
         get('folder-1').
         get('sub-folder-1.2').
         get('sub-sub-folder-1-2.1').
         contentItems()],
    )

    # remove all sub items from the last sub folder.
    remove_folders.extend(
        [i[1] for i in portal.
         get('folder-2').
         get('sub-folder-2.5').
         contentItems()],
    )

    # remove all sub items from the last sub sub folder.
    remove_folders.extend(
        [i[1] for i in portal.
         get('folder-2').
         get('sub-folder-2.1').
         get('sub-sub-folder-2-1.5').
         contentItems()],
    )

    # make a top folder with a different amount of sub items.
    remove_folders.extend(
        [i[1] for i in portal.
         get('folder-3').
         contentItems()[-2:]],
    )

    # remove all sub items from a sub folder in between.
    remove_folders.extend(
        [i[1] for i in portal.
         get('folder-3').
         get('sub-folder-3.2').
         contentItems()],
    )

    # remove all sub sub items from a sub folder in between.
    remove_folders.extend(
        [i[1] for i in portal.
         get('folder-3').
         get('sub-folder-3.1').
         get('sub-sub-folder-3-1.3').
         contentItems()],
    )

    # lets remove all sub items from a top folder
    remove_folders.extend(
        [i[1] for i in portal.
         get('folder-4').
         contentItems()],
    )

    api.content.delete(objects=remove_folders, check_linkintegrity=False)
