from typing import Any
from zope.interface import Interface, Attribute,implementedBy, providedBy

import repositorys.i_base

class IBase(Interface):
    repository = Attribute("Repository to access the database")

class BaseService:

    def __init__(self, repository) -> None:
        self.repository: repositorys.i_base.IBase = repository
