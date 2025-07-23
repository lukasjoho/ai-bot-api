from pydantic import BaseModel, Field
from typing import Literal, Union

# Text message

class TextMessageData(BaseModel):   
    text: str = Field(description="The text content to send to the user")

class TextMessage(BaseModel):
    """Standard text message - use this for most responses"""
    type: Literal["text"] = Field(default="text", description="Message type identifier")
    data: TextMessageData

# Image message

class ImageMessageData(BaseModel):
    image_url: str = Field(description="URL of the image to send")
    caption: str = Field(description="Caption for the image")

class ImageMessage(BaseModel):
    """Image message with optional caption"""
    type: Literal["image"] = Field(default="image", description="Message type identifier")
    data: ImageMessageData

# Reaction message

class ReactionMessageData(BaseModel):
    emoji: str = Field(description="Emoji to send to the user")
    message_id: str = Field(description="ID of the message to send the reaction to")

class ReactionMessage(BaseModel):
    type: Literal["reaction"] = Field(default="reaction", description="Message type identifier")
    data: ReactionMessageData

# Error message

class ErrorMessageData(BaseModel):
    message_type: Literal["ratelimit", "exception"] = Field(description="Type of error message to send")
    custom_message: str | None = Field(default=None, description="Custom error message to send")

class ErrorMessage(BaseModel):
    type: Literal["error"] = Field(default="error", description="Message type identifier")
    data: ErrorMessageData

# Typing message

class TypingMessageData(BaseModel):
    message_id: str = Field(description="ID of the message to send the typing indicator for")

class TypingMessage(BaseModel):
    type: Literal["typing"] = Field(default="typing", description="Message type identifier")
    data: TypingMessageData

# Location message

class LocationMessageData(BaseModel):
    latitude: float = Field(description="Latitude coordinate")
    longitude: float = Field(description="Longitude coordinate")
    name: str = Field(description="Name/title of the location")
    address: str = Field(description="Full address of the location")

class LocationMessage(BaseModel):
    type: Literal["location"] = Field(default="location", description="Message type identifier")
    data: LocationMessageData

# Location request message

class LocationRequestMessageData(BaseModel):
    body_text: str = Field(description="Text to display in the location request message")

class LocationRequestMessage(BaseModel):
    type: Literal["location_request"] = Field(default="location_request", description="Message type identifier")
    data: LocationRequestMessageData

# CTA message

class CTAMessageData(BaseModel):
    body_text: str = Field(description="Text to display in the CTA message")
    button_text: str = Field(description="Text for the button")
    button_url: str = Field(description="URL to redirect to when the button is clicked")

class CTAMessage(BaseModel):
    type: Literal["cta"] = Field(default="cta", description="Message type identifier")
    data: CTAMessageData

# Interactive list message

class InteractiveListMessageData(BaseModel):
    body_text: str = Field(description="Text to display in the interactive list message")
    button_text: str = Field(description="Text for the button")
    sections: list[dict] = Field(description="List of sections to display in the interactive list message")

class InteractiveListMessage(BaseModel):
    type: Literal["interactive_list"] = Field(default="interactive_list", description="Message type identifier")
    data: InteractiveListMessageData

# Interactive list section


# Agent response
class AgentResponse(BaseModel):
    """
    Response structure for WhatsApp agent interactions.
    
    The agent should generate one or more messages to send to the user via WhatsApp.
    Each message has a specific type and associated data.
    """
    
    messages: list[Union[TextMessage, ImageMessage, LocationMessage]] = Field(
        description="Array of messages to send to the user via WhatsApp. Use various message types for engaging responses.",
        min_items=1,
    )