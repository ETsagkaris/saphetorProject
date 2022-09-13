from fastapi import Depends, FastAPI, Header, Response
from typing import List
import uvicorn

from app import schemas, api, logic


app = FastAPI()
app.router.route_class = api.Wrapper


@app.get("/variants/", response_model=List[schemas.VariantInfo])
def get_variant_list(
    response: Response,
    query_params: schemas.VariantQueryParams = Depends(),
    accept: str = Header(None),
    etag: str = Header(None),
):
    api.check_accept(accept)
    api.check_etag(response, query_params, accept, etag)
    return logic.get_variant_list(query_params)


@app.post("/variants/", response_model=schemas.VariantInfo, status_code=201)
def create_variant(
    variant: schemas.VariantInput,
    authorization: str = Header(None),
):
    api.check_authorization(authorization)
    return logic.create_variant(variant)


@app.put("/variants/{ID}/",
         response_model=schemas.VariantInfo)
def edit_variant(
    ID: str,
    variant: schemas.VariantInput,
    authorization: str = Header(None),
):
    api.check_authorization(authorization)
    return logic.edit_variant(ID, variant)


@app.delete("/variants/{ID}/", status_code=204)
def remove_variant(
    ID: str,
    authorization: str = Header(None),
):
    api.check_authorization(authorization)
    return logic.delete_variant(ID)


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
