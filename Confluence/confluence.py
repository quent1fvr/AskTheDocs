import requests
import json

# Your Confluence details
base_url = "https://your-confluence-site.atlassian.net/wiki/rest/api"
auth_token = "your_api_token"
space_keys = ["SPACE1", "SPACE2"]  # List of space keys you want to index

# Headers for authentication
headers = {
    "Authorization": f"Bearer {auth_token}",
    "Accept": "application/json"
}

# Function to get pages updated after a specific date
def get_updated_pages(space_key, last_checked_date):
    url = f"{base_url}/content?spaceKey={space_key}&expand=version,history.lastUpdated&start=0&limit=100"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        pages = response.json()['results']
        updated_pages = [{
            'id': page['id'],
            'title': page['title']
        } for page in pages if page['history']['lastUpdated']['when'] > last_checked_date]
        return updated_pages
    else:
        print(f"Error fetching data from space {space_key}: {response.status_code}")
        return []

# Function to save data to a JSON file
def save_to_json(data):
    with open("updated_pages_across_spaces.json", "w") as file:
        json.dump(data, file, indent=4)

# Date of your last update (YYYY-MM-DD format)
last_checked_date = "2024-02-15T00:00:00.000Z"  # Adjust as needed

# Aggregate data for each space
spaces_data = {}
for space_key in space_keys:
    updated_pages = get_updated_pages(space_key, last_checked_date)
    if updated_pages:
        spaces_data[space_key] = updated_pages
        print(f"Found updated pages for space '{space_key}'.")
    else:
        print(f"No updates found for space '{space_key}'.")

# Save the aggregated data to a JSON file
if spaces_data:
    save_to_json(spaces_data)
    print("Updated pages across all spaces saved to JSON.")
else:
    print("No updates found in any of the spaces.")
