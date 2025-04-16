# Solice API

A Python package for interacting with the SolisCloud API to retrieve and store solar inverter data.

## Features

- Retrieve a list of solar inverters from SolisCloud
- Fetch detailed information about specific inverters
- Store inverter data in JSON format for analysis or integration with other systems

## Installation

### Prerequisites

- Python 3.11 or higher
- UV package manager

### Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd solice-api
   ```

2. Create and activate a virtual environment:

   ```bash
   # Create a virtual environment
   uv venv

   # Activate the virtual environment
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. Install dependencies with UV:

   ```bash
   uv sync
   ```

4. Set up configuration:
   Create a `config.json` file in the project root with your SolisCloud API credentials:
   ```json
   {
     "key": "your_api_key",
     "secret": "your_api_secret"
   }
   ```

## Usage

### Retrieve Inverter Data

Run the data retrieval script:

```bash
uv run get-data
```

This will:

1. Connect to the SolisCloud API
2. Retrieve your inverter list
3. For each inverter, fetch detailed information
4. Save each inverter's detail to a separate file (`1.json`, `2.json`, etc.) in the `data` directory

#### Notes
- Each inverter's detail is saved as a separate file for easy access and analysis.
- Files are named sequentially (`1.json`, `2.json`, ...) corresponding to the order in your inverter list. For better traceability, you may modify the code to use the inverter's serial number or ID as the filename.
- If there is an API error or a particular inverter's detail cannot be fetched, the script will skip that inverter and continue processing the rest.

## Project Structure

- `src/solice_api/main.py`: Core API functions
- `src/solice_api/__init__.py`: Package initialization and main runner function
- `data/`: Directory where inverter data is stored (created automatically)
  - `inverter_list.json`: List of all inverters
  - `1.json`, `2.json`, ...: Detail files for each inverter
- `config.json`: Configuration file for API credentials

## Dependencies

- python-dotenv (≥1.0.1)
- requests (≥2.32.3)
- soliscloud-api (≥1.2.0)

## License

[License](LICENSE)

## Contact

Muhammad Raffey - muhammadraffey26@gmail.com



