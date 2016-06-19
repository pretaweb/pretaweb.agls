from zope import schema
from zope.component import adapts
from zope.interface import alsoProvides
from zope.interface import implements
from plone.dexterity.interfaces import IDexterityContent
from plone.directives import form
from pretaweb.agls import messageFactory as _
from z3c.form.interfaces import IEditForm
from z3c.form.interfaces import IAddForm
from pretaweb.agls.content.agls import AGLS_TYPES
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

AGLS_TYPES_VOCAB = SimpleVocabulary(
    [SimpleTerm(value=x, title=_(x)) for x in AGLS_TYPES]
)

AGLS_FIELDS = (
    'agls_title_override', 'agls_title',
    'agls_desc_override', 'agls_desc',
    'creation_date',
    'agls_author_override', 'agls_author',
    'agls_id_override', 'agls_id',
    'agls_publisher_override', 'agls_publisher',
    'agls_format_override', 'agls_format'
)


class IAGLS(form.Schema):

    form.fieldset(
        'categorization',
        label=u'Categorization',
        fields=['AGLSType'],
    )

    # Main AGLS Type
    AGLSType = schema.Choice(
        title=_(u'AGLS Type'),
        description=_(u'Enter here text line to use in AGLS Type tag.'),
        required=False,
        default=None,
        missing_value=u'',
        vocabulary=AGLS_TYPES_VOCAB,
    )

    form.fieldset(
        'agls_metadata',
        label=_(u'AGLS Overrides'),
        fields=list(AGLS_FIELDS),
    )

    # AGLS Title
    agls_title_override = schema.Bool(
        title=_(u'Override AGLS Title'),
        description=_(u"By default object's title field is used."),
        required=False,
        default=False,
        missing_value=False
    )

    agls_title = schema.TextLine(
        title=_(u'AGLS Title'),
        description=_(u'Enter here custom title to use in AGLS tag.'),
        required=False,
        default=u'',
        missing_value=u''
    )

    # AGLS Description
    agls_desc_override = schema.Bool(
        title=_(u'Override AGLS Description'),
        description=_(u"By default object's description field is used."),
        required=False,
        default=False,
        missing_value=False
    )

    agls_desc = schema.Text(
        title=_(u'AGLS Description'),
        description=_(u'Enter here custom description to use in AGLS tag.'),
        required=False,
        default=u'',
        missing_value=u''
    )

    # AGLS Author
    agls_author_override = schema.Bool(
        title=_(u'Override AGLS Author'),
        description=_(u"By default object's creator field is used or global "
                      'control panel settings if configured.'),
        required=False,
        default=False,
        missing_value=False
    )

    agls_author = schema.TextLine(
        title=_(u'AGLS Author'),
        description=_(u'Enter here custom author to use in AGLS tag.'),
        required=False,
        default=u'',
        missing_value=u''
    )

    # AGLS Identifier
    agls_id_override = schema.Bool(
        title=_(u'Override AGLS Identifier'),
        description=_(u"By default object's UID attribute is used for AGLS "
                      'tag.'),
        required=False,
        default=False,
        missing_value=False
    )

    agls_id = schema.TextLine(
        title=_(u'AGLS Identifier'),
        description=_(u'Enter here custom identifier to use in AGLS tag.'),
        required=False,
        default=u'',
        missing_value=u''
    )

    # AGLS Publisher
    agls_publisher_override = schema.Bool(
        title=_(u'Override AGLS Publisher'),
        description=_(u"By default object's creator field is used or global "
                      'control panel settings if configured.'),
        required=False,
        default=False,
        missing_value=False
    )

    agls_publisher = schema.TextLine(
        title=_(u'AGLS Publisher'),
        description=_(u'Enter here custom publisher to use in AGLS tag.'),
        required=False,
        default=u'',
        missing_value=u''
    )

    # AGLS Format
    agls_format_override = schema.Bool(
        title=_(u'Override AGLS Format'),
        description=_(u"By default object's content-type will be used. Either "
                      'html or file mime-type for File/Image based content '
                      'types.'),
        required=False,
        default=False,
        missing_value=False
    )

    agls_format = schema.TextLine(
        title=_(u'AGLS Format'),
        description=_(u'Enter here custom format to use in AGLS tag.'),
        required=False,
        default=u'',
        missing_value=u''
    )

    # display fields only on edit forms
    form.omitted('AGLSType', *AGLS_FIELDS)
    form.no_omit(IEditForm, 'AGLSType', *AGLS_FIELDS)
    form.no_omit(IAddForm, 'AGLSType', *AGLS_FIELDS)

alsoProvides(IAGLS, form.IFormFieldProvider)


class BasicProperty(object):

    def __init__(self, field):
        self._field = field

    def __get__(self, inst, klass):
        if inst is None:
            return self
        return getattr(inst.context, self._field.__name__, self._field.default)

    def __set__(self, inst, value):
        setattr(inst.context, self._field.__name__, value)

    def __getattr__(self, name):
        return getattr(self._field, name)


class AGLS(object):
    implements(IAGLS)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    agls_title_override = BasicProperty(IAGLS['agls_title_override'])
    agls_title = BasicProperty(IAGLS['agls_title'])
    agls_desc_override = BasicProperty(IAGLS['agls_desc_override'])
    agls_desc = BasicProperty(IAGLS['agls_desc'])
    creation_date = BasicProperty(IAGLS['creation_date'])
    agls_author_override = BasicProperty(IAGLS['agls_author_override'])
    agls_author = BasicProperty(IAGLS['agls_author'])
    agls_id_override = BasicProperty(IAGLS['agls_id_override'])
    agls_id = BasicProperty(IAGLS['agls_id'])
    agls_publisher_override = BasicProperty(IAGLS['agls_publisher_override'])
    agls_publisher = BasicProperty(IAGLS['agls_publisher'])
    agls_format_override = BasicProperty(IAGLS['agls_format_override'])
    agls_format = BasicProperty(IAGLS['agls_format'])
    AGLSType = BasicProperty(IAGLS['AGLSType'])
