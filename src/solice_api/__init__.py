from .main import get_inverter_list, get_inverter_detail
import json
import os
import asyncio

async def main():
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Define paths
    config_path = os.path.join(project_root, 'config.json')
    data_dir = os.path.join(project_root, 'data')
    inverter_list_path = os.path.join(data_dir, 'inverter_list.json')
    inverter_detail_path = os.path.join(data_dir, 'inverter_detail.json')
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory at {data_dir}")
    
    with open(config_path, 'r') as file:
        data = json.load(file)
    api_key = data['key']
    api_secret = bytearray(data['secret'], 'utf-8')
    
    inverter_list = await get_inverter_list(api_key, api_secret)
    with open(inverter_list_path, "w") as outfile:
        json.dump(inverter_list, outfile, indent=2)
    print(f"Inverter list saved to {inverter_list_path}")
    
    with open(inverter_list_path, "r") as infile:
        inverter_data = json.load(infile)
    
    if isinstance(inverter_data, dict) and "records" in inverter_data:
        record = inverter_data["records"][0]
    elif isinstance(inverter_data, list):
        record = inverter_data[0]
    else:
        raise ValueError("Unexpected structure in inverter_list.json")
    
    inverter_id = record.get("id")
    if not inverter_id:
        raise ValueError("Inverter record does not contain required 'id'")
    
    detail = await get_inverter_detail(api_key, api_secret, inverter_id)
    
    with open(inverter_detail_path, "w") as outfile:
        json.dump(detail, outfile, indent=2)
    print(f"Inverter detail saved to {inverter_detail_path}")

def run_main():
    """Entry point for the package. Runs the main async function."""
    return asyncio.run(main())

if __name__ == "__main__":
    run_main()
