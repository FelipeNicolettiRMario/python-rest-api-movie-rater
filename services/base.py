from repositorys.interfaces import IBaseRepository


class BaseService:

    def __init__(self, repository) -> None:
        self.repository: IBaseRepository = self._check_if_repository_is_right_implemented(repository)

    def _check_if_repository_is_right_implemented(self, repository):

        if IBaseRepository.implementedBy(repository.__class__):
            return repository

        raise ValueError("Repository not implemented correctly")