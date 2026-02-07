from FastAPI import FastAPI,Depends
from pydantic import BaseModel,Field



app = FastAPI()

class PaginationParams(BaseModel):
    limit: int = Field(5,0,le=100,description ="кол-во элементов на странице")
    offset: int = Field(0,0,description ="смещение пагинации")

PaginationDep = Annotated[PaginationParams,Depends(PaginationParams)]


@app.get("/health")
async def health(
        pagination: PaginationDep
):

    await {"status": "ok"}