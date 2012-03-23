from Acquisition import aq_inner

from zope.component import getUtility
from Products.Five.browser import BrowserView

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.utils import safe_unicode
from Products.Archetypes.utils import shasattr

from plone.registry.interfaces import IRegistry
from plone.app.layout.viewlets.common import DublinCoreViewlet

from pretaweb.agls.config import AGLS_SCHEME


class AGLSView(BrowserView):

    def Title(self):
        context = aq_inner(self.context)

        # AGLS Title
        if shasattr(context, 'agls_title_override') and \
           context.agls_title_override:
            return context.agls_title
        else:
            return None

    def Description(self):
        context = aq_inner(self.context)

        # AGLS Description
        if shasattr(context, 'agls_desc_override') and \
           context.agls_desc_override:
            return context.agls_desc
        else:
            return None

    def Created(self):
        context = aq_inner(self.context)

        # AGLS Date
        value = ''
        if shasattr(context, 'creation_date'):
            value = context.creation_date
            # try to convert value to ISO8601 format w/o time component
            if hasattr(value, 'strftime'):
                value = value.strftime('%Y-%m-%d')
            else:
                value = ''
        return value

    def Creator(self):
        context = aq_inner(self.context)

        # get global AGLS settings
        registry = getUtility(IRegistry)
        import pdb; pdb.set_trace()

        # AGLS Author
        default_author = registry[
            'pretaweb.agls.browser.controlpanel.IAGLSSchema.default_author']
        if shasattr(context, 'agls_author_override') and \
           context.agls_author_override:
            value = context.agls_author
        elif default_author:
            value = default_author
        else:
            value = None
        return value

    def Subject(self):
        context = aq_inner(self.context)

        # AGLS Subject
        if shasattr(context, 'agls_subject_override') and \
           context.agls_subject_override:
            value = '; '.join(context.agls_subject)
        else:
            value = ''
        return value

    def Type(self):
        context = aq_inner(self.context)

        # AGLS Type
        value = ''
        if shasattr(context, 'agls_type_override') and \
           context.agls_type_override:
            value = context.agls_type
        elif shasattr(context, 'AGLSType'):
            value = context.AGLSType
        return safe_unicode(value)

    def Identifier(self):
        context = aq_inner(self.context)

        # AGLS Identifier
        if shasattr(context, 'agls_id_override') and \
           context.agls_id_override:
            value = u'urn:uuid:' + safe_unicode(context.agls_id)
        elif shasattr(context, 'UID'):
            value = u'urn:uuid:' + safe_unicode(context.UID())
        else:
            value = safe_unicode(context.absolute_url())
        return value

    def Publisher(self):
        context = aq_inner(self.context)
        # get global AGLS settings
        registry = getUtility(IRegistry)

        # AGLS Publisher
        default_publisher = registry[
            'pretaweb.agls.browser.controlpanel.IAGLSSchema.default_publisher']
        if shasattr(context, 'agls_publisher_override') and \
           context.agls_publisher_override:
            value = context.agls_publisher
        elif default_publisher:
            value = default_publisher
        else:
            value = None
        return safe_unicode(value)

    def Format(self):
        context = aq_inner(self.context)
        # get global AGLS settings
        registry = getUtility(IRegistry)

        # AGLS Format
        if shasattr(context, 'agls_format_override') and \
           context.agls_format_override:
            value = context.agls_format
        else:
            value = None
        return safe_unicode(value)
