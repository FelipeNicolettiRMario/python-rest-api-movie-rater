from services import *
from services.interfaces import *

from repositorys import *
from repositorys.interfaces import *


class Factory:

    def __init__(self) -> None:
        self.material = self._get_material()

    def _get_material(self):
        material = dict()

        material.update({IBaseRepository:BaseRepository})
        material.update({ICastRepository:CastRepository})
        material.update({IImageRepository:ImageRepository})

        material.update({IBaseService:BaseService})
        material.update({ICastService:CastService})
        material.update({IImageService:ImageService})
        material.update({IMovieService:MovieService})
        material.update({IParticipantService:ParticipantService})
        material.update({IUserService:UserService})

        return material

    def add_material(self, interface, implementation):
        self.material.update({interface:implementation})

    def produce_service_with_repository(self, repository_interface, service_interface, db_session) -> IBaseService:

        repository = self.material.get(repository_interface)(db_session)
        service = self.material.get(service_interface)(repository)

        return service

    def produce_service_with_repository_and_image_service(self, 
        repository_interface, 
        service_interface,
        image_service_interface,
        image_service_repository_interface, 
        db_session) -> IBaseService:
        
        repository = self.material.get(repository_interface)(db_session)
        
        image_repository = self.material.get(image_service_repository_interface)(db_session)
        image_service = self.material.get(image_service_interface)(image_repository)

        service = self.material.get(service_interface)(repository,image_service)

        return service

