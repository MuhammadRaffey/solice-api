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

    # Support both dict with 'records' or plain list
    if isinstance(inverter_data, dict) and "records" in inverter_data:
        records = inverter_data["records"]
    elif isinstance(inverter_data, list):
        records = inverter_data
    else:
        raise ValueError("Unexpected structure in inverter_list.json")

    for idx, record in enumerate(records, start=1):
        inverter_id = record.get("id")
        if not inverter_id:
            print(f"Skipping record {idx} without 'id'")
            continue
        detail = await get_inverter_detail(api_key, api_secret, inverter_id)
        detail_path = os.path.join(data_dir, f"{idx}.json")
        with open(detail_path, "w") as outfile:
            json.dump(detail, outfile, indent=2)
        print(f"Inverter detail for inverter {inverter_id} saved to {detail_path}")

def run_main():
    """Entry point for the package. Runs the main async function."""
    return asyncio.run(main())

if __name__ == "__main__":
    run_main()
