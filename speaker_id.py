import requests

url = "https://api.genny.lovo.ai/api/v1/speakers?sort=displayName%3A1"

headers = {
    "accept": "application/json",
    "X-API-KEY": "e6302ca5-4fb3-4e12-a461-80b821e3dc4f"
}

response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()["data"]
    
    # Define the conditions for filtering
    desired_gender = "male"  # Change this to the desired gender
    desired_locale = "en-IN"  # Change this to the desired locale
    
    # Filter the data based on gender and locale
    filtered_data = [item["id"] for item in data if item["gender"] == desired_gender and item["locale"] == desired_locale]
    
    # Print the filtered IDs
    for speaker_id in filtered_data:
        print("Speaker ID:", speaker_id)
else:
    print("Error:", response.status_code, response.text)
