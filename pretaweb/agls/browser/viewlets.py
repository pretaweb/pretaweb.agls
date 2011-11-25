from Acquisition import aq_inner

from zope.component import getUtility

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.utils import safe_unicode
from Products.Archetypes.utils import shasattr

from plone.registry.interfaces import IRegistry
from plone.app.layout.viewlets.common import DublinCoreViewlet

from pretaweb.agls.config import AGLS_SCHEME


class AGLSViewlet(DublinCoreViewlet):
    index = ViewPageTemplateFile('templates/agls.pt')
    
    def update(self):
        super(AGLSViewlet, self).update()
        
        # DC tags are switched off in Plone control panel
        if not self.metatags:
            return
        
        # map dublin core meta tags
        dc = {}
        for tag in self.metatags:
            dc[tag[0]] = tag[1]
        
        context = aq_inner(self.context)
        agls_tags = []
        
        # AGLS Title
        if shasattr(context, 'agls_title_override') and \
           context.agls_title_override:
            value = context.agls_title
        else:
            value = dc.get('DC.Title', '') or context.Title()
        agls_tags.append({
            'name': u'DCTERMS.title',
            'content': safe_unicode(value),
            'scheme': AGLS_SCHEME['DCTERMS.title']
        })
        
        # AGLS Description
        if shasattr(context, 'agls_desc_override') and \
           context.agls_desc_override:
            value = context.agls_desc
        else:
            value = dc.get('DC.description', '')
        agls_tags.append({
            'name': u'DCTERMS.description',
            'content': safe_unicode(value),
            'scheme': AGLS_SCHEME['DCTERMS.description']
        })
        agls_tags.append({
            'name': u'description',
            'content': safe_unicode(value),
            'scheme': AGLS_SCHEME['description']
        })
        
        # AGLS Date
        if shasattr(context, 'agls_date_override') and \
           context.agls_date_override:
            value = context.agls_date
        else:
            value = dc.get('DC.date.created', '')
        # try to convert value to ISO8601 format
        if hasattr(value, 'ISO8601'):
            # zope DateTime
            value = value.ISO8601()
        elif hasattr(value, 'isoformat'):
            # python datetime
            value = value.isoformat()
        agls_tags.append({
            'name': u'DCTERMS.created',
            'content': value or '',
            'scheme': AGLS_SCHEME['DCTERMS.created']
        })
        
        # get global AGLS settings
        registry = getUtility(IRegistry)
        
        # AGLS Author
        default_author = registry[
            'pretaweb.agls.browser.controlpanel.IAGLSSchema.default_author']
        if shasattr(context, 'agls_author_override') and \
           context.agls_author_override:
            value = context.agls_author
        elif default_author:
            value = default_author
        else:
            value = dc.get('DC.creator', '')
        agls_tags.append({
            'name': u'DCTERMS.creator',
            'content': safe_unicode(value),
            'scheme': AGLS_SCHEME['DCTERMS.creator']
        })
        
        # AGLS Subject
        if shasattr(context, 'agls_subject_override') and \
           context.agls_subject_override:
            value = '; '.join(context.agls_subject)
        else:
            value = '; '.join(dc.get('DC.subject', '').split(', '))
        agls_tags.append({
            'name': u'DCTERMS.subject',
            'content': safe_unicode(value),
            'scheme': AGLS_SCHEME['DCTERMS.subject']
        })
        
        # AGLS Type
        value = ''
        if shasattr(context, 'agls_type_override') and \
           context.agls_type_override:
            value = ', '.join(context.agls_type)
        elif shasattr(context, 'AGLSType'):
            value = ', '.join(context.AGLSType)
        agls_tags.append({
            'name': u'DCTERMS.type',
            'content': safe_unicode(value),
            'scheme': AGLS_SCHEME['DCTERMS.type']
        })
        
        # AGLS Identifier
        if shasattr(context, 'agls_id_override') and \
           context.agls_id_override:
            value = context.agls_id
        elif shasattr(context, 'UID'):
            value = context.UID()
        else:
            value = context.getId()
        agls_tags.append({
            'name': u'DCTERMS.identifier',
            'content': u'urn:uuid:' + safe_unicode(value),
            'scheme': AGLS_SCHEME['DCTERMS.identifier']
        })
        
        # copy over keywords tag
        if 'keywords' in dc:
            agls_tags.append({
                'name': u'keywords',
                'content': safe_unicode(dc['keywords']),
                'scheme': None
            })
        
        # AGLS Publisher
        default_publisher = registry[
            'pretaweb.agls.browser.controlpanel.IAGLSSchema.default_publisher']
        if shasattr(context, 'agls_publisher_override') and \
           context.agls_publisher_override:
            value = context.agls_publisher
        elif default_publisher:
            value = default_publisher
        else:
            value = dc.get('DC.creator', '') or context.Creator()
        agls_tags.append({
            'name': u'DCTERMS.publisher',
            'content': safe_unicode(value),
            'scheme': AGLS_SCHEME['DCTERMS.publisher']
        })

        # AGLS Format
        if shasattr(context, 'agls_format_override') and \
           context.agls_format_override:
            value = context.agls_format
        else:
            value = dc.get('DC.format', '')
        agls_tags.append({
            'name': u'DCTERMS.format',
            'content': safe_unicode(value),
            'scheme': AGLS_SCHEME['DCTERMS.format']
        })

        self.metatags = tuple(agls_tags)
