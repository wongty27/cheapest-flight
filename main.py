from typing import Annotated

from fastapi import FastAPI, File, Query, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


class FlightObject(BaseModel):
    src: Annotated[int, Field(ge=0)]
    dst: Annotated[int, Field(ge=0)]
    price: Annotated[float, Field(ge=0)]


class InputData(BaseModel):
    n: Annotated[int, Field(ge=0)]
    flights: list[FlightObject]

    @field_validator("flights")
    @classmethod
    def validate_flights(cls, v):
        for f in v:
            if isinstance(f, list) and len(f) != 3:
                raise ValueError("Flight data format must be [src, dst, price]")
        return v


limiter = Limiter(key_func=get_remote_address)


app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(CORSMiddleware, allow_methods=["POST", "GET"])
# app.add_middleware(SlowAPIMiddleware)


@app.post("/flight")
@limiter.limit("12/minute")
async def get_cheap_flight(
    request: Request,
    src: int = Query(description="Source city"),
    dst: int = Query(description="Destination city"),
    k: int = Query(ge=0, description="Max stops"),
    file: UploadFile = File(...),
):
    # Json file parsing
    content = await file.read()
    data = InputData.model_validate_json(content)
    # data = json.loads(content)

    n = data.n
    flights = parse_flights(data.flights)
    price = bellman_ford(n, flights, src, dst, k)
    return {"src": src, "dst": dst, "price": price}


def parse_flights(flights):
    parsed = []
    for f in flights:
        if isinstance(f, FlightObject):
            # force type safety
            parsed.append((f.src, f.dst, f.price))
        elif isinstance(f, list):
            u, v, w = map(int, f)
            parsed.append((u, v, w))
        else:
            raise ValueError("Invalid flight format")
    return parsed


def bellman_ford(n, flights, src, dst, k):
    prices = [float("inf")] * n
    prices[src] = 0

    for _ in range(k + 1):
        temp = prices.copy()

        for u, v, w in flights:
            if prices[u] == float("inf"):
                continue

            if prices[u] + w < temp[v]:
                temp[v] = prices[u] + w

        prices = temp

    return prices[dst] if prices[dst] != float("inf") else -1
