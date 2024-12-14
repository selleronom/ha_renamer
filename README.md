# Home Assistant Entity Renamer

This script renames Home Assistant entities based on their friendly names. It filters out lights that do not have a `hue_type` attribute and renames them to match their friendly names.

## Prerequisites

- Python 3.12+
- Home Assistant instance
- Long-lived access token for Home Assistant

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/selleronom/ha_renamer.git
    cd ha_renamer
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    source .venv/bin/activate
    ```

3. Install the required packages using [pyproject.toml](https://til.simonwillison.net/python/pyproject):
    ```sh
    pip install .
    ```

4. Create a [.env](https://blog.enterprisedna.co/python-dotenv/) file in the project directory with the following content:
    ```env
    HA_URL=http://homeassistant.local:8123
    HA_TOKEN=your_long_lived_access_token
    ```

## Usage

1. Run the script:
    ```sh
    python hello.py
    ```

2. The script will print the intended renaming actions. Uncomment the line in the script to actually perform the renaming.

## Example

Given an entity with the following attributes:
```json
{
  "entity_id": "light.hue_color_lamp_1_3",
  "attributes": {
    "friendly_name": "Living Room Ceiling 1"
  }
}
```

The script will rename it to:
```
light.living_room_ceiling_1
```

## Notes

- The script uses the `python-dotenv` library to load environment variables from a `.env` file.
- The WebSocket URL is constructed based on the `HA_URL` environment variable.

## License

This project is licensed under the MIT License.