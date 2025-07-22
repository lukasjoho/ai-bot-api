import os
from agents import function_tool
from agents.tool import FileSearchTool, WebSearchTool
from services.database.types import Product, Store, Tip
from services.database.database import get_data
from dotenv import load_dotenv

load_dotenv()

def create_knowledge_tools():
    @function_tool
    def get_all_stores() -> list[Store]:
        """Get all on-site Belcando stores from the database. Can be used to list all, or to get information about only 1 or 2 nearby.
        
        Return example:
        [
            {
                "id": "store_001",
                "name": "Belcando Store Berlin",
                "latitude": 52.52437,
                "longitude": 13.41053,
                "address": {    
                    "street": "Kurfürstendamm 100",
                    "zipcode": "10707",
                    "city": "Berlin"
                }
            }
        ]
        """
        return get_data("stores.json")
    
    @function_tool
    def get_all_products() -> list[Product]:
        """Get all products from the database. Can be used to list all, or to get information about only 1 or 2.
        
        Return example:
        [
            {
                "id": "product_001",
                "imageUrl": "https://d23dsm0lnesl7r.cloudfront.net/media/bc/46/92/1744020374/bb-klp-2023-adult-active-800px.jpg",
                "title": "Dog Box BELCANDO Adult Active",
                "price": "4,99€"
            }
        ]
        """
        return get_data("products.json")
    
    @function_tool
    def get_all_tips() -> list[Tip]:
        """Get all tips and tricks from the database. They are blogposts from the website showing how to take care of your dogs.
        
        Return example:
        
        [
            {
                "id": "tip_001",
                "image": "https://d23dsm0lnesl7r.cloudfront.net/media/6d/09/43/1731491803/blog-puppy-blues.jpg",
                "title": "Von Welpenfreude zu Welpenfrust: Was ist \"Puppy Blues\"?",
                "description": "Wie die anfängliche Freude am neuen Welpen in den 'Puppy Blues' umschlagen kann und wie frischgebackene Hundebesitzer damit umgehen können",
                "url": "https://www.belcando.de/pfotentipps/frust-mit-welpen",
                "cta": "Mehr lesen"
            }
        ]
        """
        return get_data("tips.json")
    
    knowledge_tools = [get_all_stores, get_all_products, get_all_tips]
    
    # Add FileSearchTool if vector store is available
    vector_store_id = os.getenv("OPENAI_VECTOR_STORE_ID")
    if vector_store_id:
        file_search_tool = FileSearchTool(vector_store_ids=[vector_store_id])
        knowledge_tools.append(file_search_tool)

    website_search_tool = WebSearchTool()
    knowledge_tools.append(website_search_tool)
    
    return knowledge_tools