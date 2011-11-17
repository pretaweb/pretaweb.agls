from Products.Five.browser import BrowserView

class AGLSControlPanelView(BrowserView):
    
    def __call__(self):
        return u"Hello world!"
