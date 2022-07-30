from zope.interface import Interface, Attribute

class IUserService(Interface):
    image_service = Attribute("Service to manage user picture")