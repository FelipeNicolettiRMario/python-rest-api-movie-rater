from zope.interface import Interface, Attribute

class IParticipantService(Interface):
    image_service = Attribute("Service to manage participant picture")