from pydantic import TypeAdapter
from services.whatsapp.dispatcher import dispatch_message
from services.whatsapp.types import AgentResponse

async def process_stream(result, phone_number: str):

    # Set up partial validation
    response_adapter = TypeAdapter(AgentResponse)
    accumulated_json = ""
    sent_messages = set()  # Track already sent messages to avoid duplicates
    async for event in result.stream_events():
        if event.type == "raw_response_event" and event.data.type == "response.output_text.delta":
            # Accumulate JSON delta
            accumulated_json += event.data.delta            
            # Try partial validation
            try:
                partial_response = response_adapter.validate_json(
                    accumulated_json, 
                    experimental_allow_partial=True
                )
                
                # Dispatch any newly validated messages immediately
                for i, msg in enumerate(partial_response.messages):
                    if i not in sent_messages:
                        # Only dispatch messages with valid content
                        print("Dispatching message...", msg)
                        success = dispatch_message(phone_number, msg)
                        if success:
                            sent_messages.add(i)
            except Exception:
                continue

    return result