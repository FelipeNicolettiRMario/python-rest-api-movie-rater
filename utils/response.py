from fastapi.responses import JSONResponse

def create_response(status_code: int = 200, body: dict = dict()) -> JSONResponse:

    return JSONResponse(body, status_code)