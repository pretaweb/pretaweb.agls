# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

import logging

# The profile id of your package:
PROFILE_ID = 'profile-pretaweb.agls:default'


def add_catalog_indexes(context, logger=None):
    """Method to add our wanted indexes to the portal_catalog.

    @parameters:

    When called from the import_various method below, 'context' is
    the plone site and 'logger' is the portal_setup logger.  But
    this method can also be used as upgrade step, in which case
    'context' will be portal_setup and 'logger' will be None.
    """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('pretaweb.agls')

    # Run the catalog.xml step as that may have defined new metadata
    # columns.  We could instead add <depends name="catalog"/> to
    # the registration of our import step in zcml, but doing it in
    # code makes this method usable as upgrade step as well.  Note that
    # this silently does nothing when there is no catalog.xml, so it
    # is quite safe.
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')

    catalog = getToolByName(context, 'portal_catalog')
    indexes = catalog.indexes()
    # Specify the indexes you want, with ('index_name', 'index_type')
    wanted = (('agls_type', 'FieldIndex'),
              )
    indexables = []
    for name, meta_type in wanted:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            logger.info('Added %s for field %s.', meta_type, name)
        indexables.append(name)
    if len(indexables) > 0:
        logger.info('Indexing new indexes %s.', ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


def install(context):
    """Import step for configuration that is not handled in xml files."""
    # Only run step if a flag file is present
    if not context.readDataFile('pretaweb.agls.default.txt'):
        return

    logger = context.getLogger('pretaweb.agls')
    site = context.getSite()
    add_catalog_indexes(site, logger)


def uninstall(context):
    """Install step for configuration that is not handled in xml files."""
    # Only run step if a flag file is present
    if not context.readDataFile('pretaweb.agls.uninstall.txt'):
        return

    logger = context.getLogger('pretaweb.agls')
    site = context.getSite()

    catalog = getToolByName(site, 'portal_catalog')
    # old collections
    atct = getToolByName(site, 'portal_atct')
    indexes = catalog.indexes()
    # Specify the indexes you want, with ('index_name', 'index_type')
    wanted = (('agls_type ', 'FieldIndex'),
              )
    for name, meta_type in wanted:
        if name in indexes:
            catalog.delIndex(name)
            logger.info('Removed %s for field %s.', meta_type, name)
            # old collections
            atct.removeIndex(name)
            atct.removeMetadata(name)
            logger.info(
                'Removed %s for old collection field %s.', meta_type, name)
