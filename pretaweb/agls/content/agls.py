from zope.component import adapts
from zope.interface import implements

from Products.Archetypes.interfaces import IBaseContent
from Products.Archetypes import public as atapi

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender, \
    ISchemaExtender, ISchemaModifier

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
            schemata="AGLS Metadata",
            widget=atapi.BooleanWidget(
                label=_(u"Override AGLS Title"),
                description=_(u"By default object's title field is used.")
            ),
            required=False,
            default=False
        ),
        ExtensionStringField("agls_title",
            schemata="AGLS Metadata",
            widget=atapi.StringWidget(
                label=_(u"AGLS Title"),
                description=_(u"Enter here custom title to use in AGLS tag.")
            ),
            required=False,
            default=''
        ),
        
        # AGLS Description
        ExtensionBooleanField("agls_desc_override",
            schemata="AGLS Metadata",
            widget=atapi.BooleanWidget(
                label=_(u"Override AGLS Description"),
                description=_(u"By default object's description field is used.")
            ),
            required=False,
            default=False
        ),
        ExtensionTextField("agls_desc",
            schemata="AGLS Metadata",
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
        
        # AGLS Author
        ExtensionBooleanField("agls_author_override",
            schemata="AGLS Metadata",
            widget=atapi.BooleanWidget(
                label=_(u"Override AGLS Author"),
                description=_(u"By default object's creator field is used or "
                              "global control panel settings if configured.")
            ),
            required=False,
            default=False
        ),
        ExtensionStringField("agls_author",
            schemata="AGLS Metadata",
            widget=atapi.StringWidget(
                label=_(u"AGLS Author"),
                description=_(u"Enter here custom author to use in AGLS tag.")
            ),
            required=False,
            default=''
        ),
        
        # AGLS Type
        ExtensionBooleanField("agls_type_override",
            schemata="AGLS Metadata",
            widget=atapi.BooleanWidget(
                label=_(u"Override AGLS Type"),
                description=_(u"By default object's AGLS Type, from "
                              "Categorization tab, field is used in AGLS tag.")
            ),
            required=False,
            default=False
        ),
        ExtensionStringField("agls_type",
            schemata="AGLS Metadata",
            widget=atapi.StringWidget(
                label=_(u"AGLS Type"),
                description=_(u"Enter here custom Type to use in AGLS Type "
                              "Tag."),
            ),
            required=False,
            default=''
        ),
        ExtensionStringField("AGLSType",
            schemata="categorization",
            widget=atapi.StringWidget(
                label=_(u"AGLS Type"),
                description=_(u"Enter here text line to use in AGLS Type tag.")
            ),
            required=False,
            default=''
        ),
        
        # AGLS Identifier
        ExtensionBooleanField("agls_id_override",
            schemata="AGLS Metadata",
            widget=atapi.BooleanWidget(
                label=_(u"Override AGLS Identifier"),
                description=_(u"By default object's UID attribute is used for "
                              "AGLS tag.")
            ),
            required=False,
            default=False
        ),
        ExtensionStringField("agls_id",
            schemata="AGLS Metadata",
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
            schemata="AGLS Metadata",
            widget=atapi.BooleanWidget(
                label=_(u"Override AGLS Publisher"),
                description=_(u"By default object's creator field is used or "
                              "global control panel settings if configured.")
            ),
            required=False,
            default=False
        ),
        ExtensionStringField("agls_publisher",
            schemata="AGLS Metadata",
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
            schemata="AGLS Metadata",
            widget=atapi.BooleanWidget(
                label=_(u"Override AGLS Format"),
                description=_(u"By default object's content-type will be used. "
                              "Either html or file mime-type for File/Image "
                              "based content types.")
            ),
            required=False,
            default=False
        ),
        ExtensionStringField("agls_format",
            schemata="AGLS Metadata",
            widget=atapi.StringWidget(
                label=_(u"AGLS Format"),
                description=_(u"Enter here custom format to use in AGLS "
                              "tag.")
            ),
            required=False
        ),
        
    ]

    def __init__(self, context):
        self.context = context
    
    def getFields(self):
        """Return list of new fields we contribute to content"""
        return self.fields

class AGLSModifier(object):
    """Here we update creation date field to display it under AGLS tab"""

    adapts(IBaseContent)
    implements(ISchemaModifier, IBrowserLayerAwareExtender)
    
    layer = IPackageLayer
    
    def __init__(self, context):
        self.context = context
        
    def fiddle(self, schema):
        if schema.get('creation_date', None) is None:
            return
        
        # move to AGLS schemata
        schema['creation_date'].schemata = 'AGLS Metadata'
        
        # update desctiption
        schema['creation_date'].widget.description = _(u"Date this "
            "object was created. Used for AGLS Date meta tag.")
            
        # unhide it
        schema['creation_date'].widget.visible = {'edit': 'visible',
            'view': 'invisible'}
        
        # set starting year
        schema['creation_date'].widget.starting_year = 1990
        
        # move after AGLS description field
        schema.moveField('creation_date', after='agls_desc')
