from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.Widget import KeywordWidget


class MultipleIndexKeywordWidget(KeywordWidget):
    _properties = KeywordWidget._properties.copy()
    _properties.update({
        'macro' : "multipleindexkeyword_widget",
        'indexes': () # list of catalog indexes to get existing keywords from
        })

    security = ClassSecurityInfo()

    security.declarePublic('getExistingKeywords')
    def getExistingKeywords(self, context, fieldName, accessor, vocab_source):
        """Returns existing keywords from catalog indexes"""
        if len(self.indexes) == 0:
            return ()
        
        # if enforce then do not add any extra keywords
        allowed, enforce = context.Vocabulary(fieldName)
        result = allowed.values()
        
        if not enforce:
            catalog = getToolByName(context, vocab_source)
            for index in self.indexes:
                result += catalog.uniqueValuesFor(index)
        
        # remove duplicates
        result = [term for term in set(result)]
        result.sort()
        
        return result
