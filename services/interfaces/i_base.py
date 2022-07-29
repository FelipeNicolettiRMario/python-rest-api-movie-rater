from zope.interface import Interface, Attribute

class IBase(Interface):
    repository = Attribute("Repository to access the database")
