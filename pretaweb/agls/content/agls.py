from zope.component import adapts
from zope.interface import implements

from Products.Archetypes.interfaces import IBaseContent
from Products.Archetypes import public as atapi

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender, \
    ISchemaExtender

from pretaweb.agls.form.widget import MultipleIndexKeywordWidget
from pretaweb.agls.browser.interfaces import IPackageLayer
from pretaweb.agls import messageFactory as _

# extender AT fields
class ExtensionBooleanField(ExtensionField, atapi.BooleanField):
    """Retrofitted boolean field"""

class ExtensionStringField(ExtensionField, atapi.StringField):
    """Retrofitted string field"""

class ExtensionTextField(ExtensionField, atapi.TextField):
    """Retrofitted text field"""

class ExtensionLinesField(ExtensionField, atapi.LinesField):
    """Retrofitted lines field"""

class ExtensionDateTimeField(ExtensionField, atapi.DateTimeField):
    """Retrofitted datetime field"""


# AGLS fields extender
class AGLSExtender(object):
    """Adds AGLS fields to all archetypes objects that are used to override
    AGLA meta tags on a page on per object bases.
    """
    
    adapts(IBaseContent)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)
    
    layer = IPackageLayer
    
    fields = [
        # AGLS Title
        ExtensionBooleanField("agls_title_override",
            schemata="agls",
            widget=atapi.BooleanWidget(
                label=_(u"Override AGLS Title"),
                description=_(u"By default object's title field is used.")
            ),
            required=False,
            default=False
        ),
        ExtensionStringField("agls_title",
            schemata="agls",
            widget=atapi.StringWidget(
                label=_(u"AGLS Title"),
                description=_(u"Enter here custom title to use in AGLS tag.")
            ),
            required=False,
            default=''
        ),
        
        # AGLS Description
        ExtensionBooleanField("agls_desc_override",
            schemata="agls",
            widget=atapi.BooleanWidget(
                label=_(u"Override AGLS Description"),
                description=_(u"By default object's description field is used.")
            ),
            required=False,
            default=False
        ),
        ExtensionTextField("agls_desc",
            schemata="agls",
            default_content_type='text/plain',
            allowable_content_types=('text/plain',),
            widget=atapi.TextAreaWidget(
                label=_(u"AGLS Description"),
                description=_(u"Enter here custom description to use in AGLS "
                              "tag.")
            ),
            required=False,
            default=''
        ),
        
        # AGLS Date
        ExtensionBooleanField("agls_date_override",
            schemata="agls",
            widget=atapi.BooleanWidget(
                label=_(u"Override AGLS Date"),
                description=_(u"By default object's creation date field is "
                              "used.")
            ),
            required=False,
            default=False
        ),
        ExtensionDateTimeField("agls_date",
            schemata="agls",
            widget=atapi.CalendarWidget(
                label=_(u"AGLS Date"),
                description=_(u"Enter here custom date to use in AGLS "
                              "tag.")
            ),
            required=False
        ),
        
        # AGLS Author
        ExtensionBooleanField("agls_author_override",
            schemata="agls",
            widget=atapi.BooleanWidget(
                label=_(u"Override AGLS Author"),
                description=_(u"By default object's creator field is used or "
                              "global control panel settings if configured.")
            ),
            required=False,
            default=False
        ),
        ExtensionStringField("agls_author",
            schemata="agls",
            widget=atapi.StringWidget(
                label=_(u"AGLS Author"),
                description=_(u"Enter here custom author to use in AGLS tag.")
            ),
            required=False,
            default=''
        ),
        
        # AGLS Subject
        ExtensionBooleanField("agls_subject_override",
            schemata="agls",
            widget=atapi.BooleanWidget(
                label=_(u"Override AGLS Subject"),
                description=_(u"By default object's keywords field is used "
                              "in AGLS tag.")
            ),
            required=False,
            default=False
        ),
        ExtensionLinesField("agls_subject",
            schemata="agls",
            accessor='agls_subject',
            multivalued=1,
            widget=MultipleIndexKeywordWidget(
                label=_(u"AGLS Subject"),
                description=_(u"Enter here custom keywords to use in AGLS "
                              "tag."),
                indexes=('Subject', 'agls_subject')
            ),
            required=False
        ),
        
        # AGLS Type
        ExtensionBooleanField("agls_type_override",
            schemata="agls",
            widget=atapi.BooleanWidget(
                label=_(u"Override AGLS Type"),
                description=_(u"By default object's AGLS Type, from "
                              "Categorization tab, field is used in AGLS tag.")
            ),
            required=False,
            default=False
        ),
        ExtensionLinesField("agls_type",
            schemata="agls",
            accessor='agls_type',
            multivalued=1,
            widget=MultipleIndexKeywordWidget(
                label=_(u"AGLS Type"),
                description=_(u"Enter here list of keywords to use in AGLS "
                              "Type tag. If list is empty Type tag won't be "
                              "inserted into page."),
                indexes=('AGLSType', 'agls_type')
            ),
            required=False
        ),
        ExtensionLinesField("AGLSType",
            schemata="categorization",
            accessor='AGLSType',
            multivalued=1,
            widget=atapi.KeywordWidget(
                label=_(u"AGLS Type"),
                description=_(u"Enter here list of keywords to use in AGLS "
                              "Type tag. If list is empty Type tag won't be "
                              "inserted into page.")
            ),
            required=False
        ),
        
        # AGLS Identifier
        ExtensionBooleanField("agls_id_override",
            schemata="agls",
            widget=atapi.BooleanWidget(
                label=_(u"Override AGLS Identifier"),
                description=_(u"By default object's UID attribute is used for "
                              "AGLS tag.")
            ),
            required=False,
            default=False
        ),
        ExtensionStringField("agls_id",
            schemata="agls",
            widget=atapi.StringWidget(
                label=_(u"AGLS Identifier"),
                description=_(u"Enter here custom identifier to use in AGLS "
                              "tag.")
            ),
            required=False,
            default=''
        ),
        
        # AGLS Publisher
        ExtensionBooleanField("agls_publisher_override",
            schemata="agls",
            widget=atapi.BooleanWidget(
                label=_(u"Override AGLS Publisher"),
                description=_(u"By default object's creator field is used or "
                              "global control panel settings if configured.")
            ),
            required=False,
            default=False
        ),
        ExtensionStringField("agls_publisher",
            schemata="agls",
            widget=atapi.StringWidget(
                label=_(u"AGLS Publisher"),
                description=_(u"Enter here custom publisher to use in AGLS "
                              "tag.")
            ),
            required=False,
            default=''
        ),
        
        # AGLS Format
        ExtensionBooleanField("agls_format_override",
            schemata="agls",
            widget=atapi.BooleanWidget(
                label=_(u"Override AGLS Format"),
                description=_(u"By default 'html' string is used.")
            ),
            required=False,
            default=False
        ),
        ExtensionStringField("agls_format",
            schemata="agls",
            widget=atapi.StringWidget(
                label=_(u"AGLS Format"),
                description=_(u"Enter here custom format to use in AGLS "
                              "tag.")
            ),
            required=False,
            default='html'
        ),
        
    ]

    def __init__(self, context):
        self.context = context
    
    def getFields(self):
        """Return list of new fields we contribute to content"""
        return self.fields
