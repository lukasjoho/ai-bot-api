from fastapi import APIRouter, Request, Response, HTTPException, Query
from services.whatsapp.handler import handle_message
from services.whatsapp.verify import verify_webhook

router = APIRouter()

@router.get("/webhook")
async def webhook_get(hub_mode: str = Query(None, alias="hub.mode"),

    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")):
    try:
        # print(f"Received webhook data: {hub_mode}, {hub_verify_token}, {hub_challenge}")
        challenge = verify_webhook(hub_mode, hub_verify_token, hub_challenge)
        return Response(content=challenge)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def webhook_post(request: Request):
    #print jsonified request body
    data = await request.json()
    # print(f"Received webhook data: {data}")
    return handle_message(data)