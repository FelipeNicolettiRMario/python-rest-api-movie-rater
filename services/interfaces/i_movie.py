from zope.interface import Interface, Attribute

class IMovieService(Interface):
    image_service = Attribute("Service to manage movie poster")