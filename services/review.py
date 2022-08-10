import uuid
from fastapi.responses import JSONResponse

from models.review import Review
from services.base import BaseService
from utils.response import create_response
from utils.serializer.review import ReviewInput



class ReviewService(BaseService):

    def __init__(self, repository) -> None:
        super().__init__(repository)

    def add_review(self, review_input: ReviewInput) -> JSONResponse:
        review = self.repository.create_entity(Review,review_input.dict())

        try:
            self.repository.save_with_commit(review)
            return create_response(body=review_input.json())

        except Exception as error:
            return create_response(500,{"detail":str(error)})

    def exclude_review(self, review_id: str) -> JSONResponse:

        try:
            review_id_in_uuid_format = uuid.UUID(review_id)
            self.repository.delete_entity_from_uuid(Review, review_id_in_uuid_format)
            return create_response(body={"detail":"Review deleted with success"})

        except Exception as error:
            return create_response(500,{"detail":str(error)})

    def add_like_or_unlike_in_review(self, review_id: str, action_type:str = "like") -> JSONResponse:
        
        review_id_in_uuid_format = uuid.UUID(review_id)
        review: Review = self.repository.get_entity_by_id(Review,review_id_in_uuid_format)

        if review:

            try:
                if action_type == "like":
                    review.likes += 1
                else:
                    review.unlikes += 1   

                self.repository.update(review)
                return create_response(body={"detail":"Review updated with success"})
            
            except Exception as error:
                return create_response(500,{"detail":str(error)})
        return create_response(404,{"detail":"Review not found"})