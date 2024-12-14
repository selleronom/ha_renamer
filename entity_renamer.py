import requests
import websockets
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Replace with your Home Assistant URL and long-lived access token
HA_URL = os.getenv("HA_URL", "http://homeassistant.local:8123")
HA_TOKEN = os.getenv("HA_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

WEBSOCKET_URL = f'ws://{HA_URL.split("//")[1]}/api/websocket'

def fetch_entities():
    response = requests.get(f'{HA_URL}/api/states', headers=HEADERS)
    response.raise_for_status()
    return response.json()

async def rename_entity(entity_id, new_entity_id):
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        # Authenticate
        await websocket.send(json.dumps({
            "type": "auth",
            "access_token": HA_TOKEN
        }))
        auth_response = await websocket.recv()
        print(f"Auth response: {auth_response}")
        
        # Send rename command
        await websocket.send(json.dumps({
            "id": 1,
            "type": "config/entity_registry/update",
            "entity_id": entity_id,
            "new_entity_id": new_entity_id
        }))
        rename_response = await websocket.recv()
        print(f"Rename response: {rename_response}")

def main():
    entities = fetch_entities()
    
    # Filter lights without 'hue_type' key
    lights_to_rename = [
        e for e in entities 
        if e['entity_id'].startswith('light.') and 'hue_type' not in e['attributes']
    ]
    
    for entity in lights_to_rename:
        friendly_name = entity['attributes'].get('friendly_name', '').strip()
        new_entity_id = f"light.{friendly_name.lower().replace(' ', '_')}"
        
        # Skip renaming if the new entity ID matches the current entity ID
        if entity['entity_id'] == new_entity_id:
            print(f"Skipping renaming for {entity['entity_id']} as it matches the new entity ID")
            continue
        
        # Print intended action (dry run)
        print(f"Would rename {entity['entity_id']} to {new_entity_id}")
        print(f"Entity details: {json.dumps(entity, indent=2)}")
        
        # Uncomment this line to actually rename
        #asyncio.run(rename_entity(entity['entity_id'], new_entity_id))

if __name__ == "__main__":
    main()