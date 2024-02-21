import aiohttp
import asyncio
import pandas as pd
import re


# Function to fetch vehicle IDs
async def fetch_vehicle_ids(session):
    url = "https://sistema.warrior.com.ar:15225/api/Vehiculo/GetVehiculos"
    payload = {
        "user": "pablofederico",
        "password": "Warriorpf$$"
    }
    async with session.post(url, json=payload, ssl=False) as response:
        if response.status == 200:
            data = await response.json()
            return data
        else:
            print(f"Failed to fetch vehicle IDs, status code: {response.status}")
            return []


# Function to fetch distance data for a specific vehicle ID
async def fetch_vehicle_distance(session, veh_id):
    url = "https://sistema.warrior.com.ar:15225/api/Movimiento/GetDistancia"
    payload = {
        "user": "pablofederico",
        "password": "Warriorpf$$",
        "vehid": veh_id
    }
    async with session.post(url, json=payload, ssl=False) as response:
        if response.status == 200:
            data = await response.json()
            return data
        else:
            print(f"Failed to fetch data for vehicle ID {veh_id}, status code: {response.status}")
            return None


# Main function to orchestrate fetching vehicle IDs and their distances
async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            # Removed the infinite loop for clarity and immediate functionality demonstration
            vehicles_data = await fetch_vehicle_ids(session)
            if vehicles_data:
                # Assuming vehicles_data is a list of dicts
                # Initialize DataFrame with only the vehicle IDs initially
                df = pd.DataFrame(columns=['vehId', 'vehPatente', 'vehLabel', 'vehOdometro', 'vehHorometro'])
                for vehicle in vehicles_data:
                    veh_id = vehicle.get('vehId')  # Ensure correct key
                    veh_patente = vehicle.get('vehPatente')
                    veh_label = vehicle.get('vehLabel')
                    veh_label = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', veh_label)
                    if veh_id:
                        distance_data = await fetch_vehicle_distance(session, veh_id)
                        if distance_data:
                            # Update the DataFrame with new data, including vehPatente and vehLabel
                            new_row = [veh_id, veh_patente, veh_label, distance_data['vehOdometro'],
                                       distance_data['vehHorometro']]
                            # Merge vehicle data with distance data
                            new_row_df = pd.DataFrame([new_row], columns=['vehId', 'vehPatente', 'vehLabel',
                                                                          'vehOdometro', 'vehHorometro'])
                            df = pd.concat([df, new_row_df], ignore_index=True)
                print(df)
                df.to_csv('vehicle_data.csv', index=False)
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
