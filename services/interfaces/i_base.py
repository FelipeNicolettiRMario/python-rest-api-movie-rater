from zope.interface import Interface, Attribute

class IBaseService(Interface):
    repository = Attribute("Repository to access the database")
