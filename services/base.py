from zope.interface import Interface, Attribute

import repositorys.i_base

class IBase(Interface):
    repository = Attribute("Repository to access the database")

class BaseService:

    def __init__(self, repository) -> None:
        self.repository: repositorys.i_base.IBase = self._check_if_repository_is_right_implemented(repository)

    def _check_if_repository_is_right_implemented(self, repository):

        if repositorys.i_base.IBase.implementedBy(repository.__class__):
            return repository

        raise ValueError("Repository not implemented correctly")