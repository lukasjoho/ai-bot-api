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
    body_text: str = Field(description="Text to display to the user in the location request message, so that the user knows why they are asked for location.")

class LocationRequestMessage(BaseModel):
    type: Literal["location_request"] = Field(default="location_request", description="Message type identifier")
    data: LocationRequestMessageData

# CTA message

class CTAMessageData(BaseModel):
    body_text: str = Field(description="Text to display in the CTA message")
    button_text: str = Field(description="Text for the button", max_length=20)
    button_url: str = Field(description="URL to redirect to when the button is clicked")
    footer_text: str | None = Field(default=None, description="Text to display in the footer of the CTA message")
    header_type: Literal["text", "image"] = Field(description="Type of header to display in the CTA message")
    header_content: str = Field(description="Content of the header (text or image URL)")

class CTAMessage(BaseModel):
    type: Literal["cta"] = Field(default="cta", description="Message type identifier")
    data: CTAMessageData

# Interactive list message

class InteractiveListItem(BaseModel):
    title: str = Field(description="Primary heading of the item", max_length=24)
    description: str = Field(description="Subtext of the item", max_length=72)

class InteractiveListMessageData(BaseModel):
    header_text: str = Field(description="Title of the entire component displayed to the user")
    body_text: str = Field(description="Text to display in the interactive list message")
    button_text: str = Field(description="Text for the button. When a user taps the button in the message, it displays a modal that lists the options available.")
    items: list[InteractiveListItem] = Field(description="List of items to display in the interactive list message", min_items=1)

class InteractiveListMessage(BaseModel):
    type: Literal["interactive_list"] = Field(default="interactive_list", description="Message type identifier")
    data: InteractiveListMessageData

# Agent response
class AgentResponse(BaseModel):
    """
    Response structure for WhatsApp agent interactions.
    
    The agent should generate one or more messages to send to the user via WhatsApp.
    Each message has a specific type and associated data.
    """
    
    messages: list[Union[TextMessage, ImageMessage, LocationMessage, LocationRequestMessage, InteractiveListMessage]] = Field(
        description="Array of messages to send to the user via WhatsApp. Use various message types for engaging responses.",
        min_items=1,
    )