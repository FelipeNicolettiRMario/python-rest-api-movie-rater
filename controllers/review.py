from fastapi import Depends
from fastapi.routing import APIRouter
from repositorys.interfaces.i_base import IBaseRepository
from services.interfaces.i_review import IReviewService
from utils.factory import Factory

from utils.serializer.review import ReviewInput
from utils.session_manager import SessionManager

review = APIRouter()

@review.post("/review")
async def add_review(review:ReviewInput,
                    dbSession = Depends(SessionManager().get_session)):
    
    service_factory = Factory()
    review_service = service_factory.produce_service_with_repository(IBaseRepository,IReviewService,dbSession)

    return review_service.add_review(review)

@review.delete("/review/{review_uuid}")
async def delete_review(review_uuid: str,
                        dbSession = Depends(SessionManager().get_session)):
    
    service_factory = Factory()
    review_service = service_factory.produce_service_with_repository(IBaseRepository,IReviewService,dbSession)

    return review_service.exclude_review(review_uuid)

@review.put("/review/like/{review_uuid}")
async def like_review(review_uuid: str,
                    dbSession = Depends(SessionManager().get_session)):
    service_factory = Factory()
    review_service = service_factory.produce_service_with_repository(IBaseRepository,IReviewService,dbSession)
    return review_service.add_like_or_unlike_in_review(review_uuid)

@review.put("/review/unlike/{review_uuid}")
async def unlike_review(review_uuid: str,
                    dbSession = Depends(SessionManager().get_session)):
    service_factory = Factory()
    review_service = service_factory.produce_service_with_repository(IBaseRepository,IReviewService,dbSession)
    return review_service.add_like_or_unlike_in_review(review_uuid,"unlike")