from pydantic import BaseModel

class RestaurantReview(BaseModel):
    name: str
    review: str
    rating: int
