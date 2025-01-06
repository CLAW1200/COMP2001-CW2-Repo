import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'
import random
USERNAME = 'test_user' + str(random.randint(1, 1000000))
EMAIL = 'test@example.com' + str(random.randint(1, 1000000))
PASSWORD = 'test123' + str(random.randint(1, 1000000))

def print_response(response):
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)

# 1. Authentication
print("\n=== Testing Authentication ===")
try:
    auth_response = requests.post(
        f'{BASE_URL}/auth',
        json={
            'username': 'Tim Berners-Lee',
            'password': 'COMP2001!'
        }
    )
    print_response(auth_response)
    token = auth_response.json()['token']
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
except Exception as e:
    print(f"Authentication failed: {str(e)}")
    # Set default headers without token to continue testing
    headers = {'Content-Type': 'application/json'}

# 2. Trail Operations
print("\n=== Testing Trail Operations ===")
trail_id = None

try:
    # Create a trail with a unique name using timestamp
    new_trail = {
        'name': f'Coastal Path {random.randint(1, 1000000)}',  # Make name unique
        'length': 12.5,
        'owner_id': 1
    }
    create_trail_response = requests.post(
        f'{BASE_URL}/trail',
        headers=headers,
        json=new_trail
    )
    print("Creating trail:")
    print_response(create_trail_response)
    trail_id = create_trail_response.json().get('id')  # Use .get() for safety
    
    if not trail_id:
        raise Exception("Failed to get trail_id from response")
except Exception as e:
    print(f"Failed to create trail: {str(e)}")

# Get all trails
print("Getting all trails:")
print_response(requests.get(f'{BASE_URL}/trail'))

# Fix 404s by checking trail_id exists
if trail_id:
    try:
        # Get specific trail
        print(f"Getting trail {trail_id}:")
        print_response(requests.get(f'{BASE_URL}/trail/{trail_id}'))

        # Update trail
        updated_trail = {
            'name': f'Updated Coastal Path {random.randint(1, 1000000)}',  # Keep name unique
            'length': 13.0,
            'owner_id': 1
        }
        print("Updating trail:")
        print_response(requests.put(
            f'{BASE_URL}/trail/{trail_id}',
                headers=headers,
                json=updated_trail
            ))
    except Exception as e:
        print(f"Failed to update trail: {str(e)}")

# 3. Location Operations
print("\n=== Testing Location Operations ===")
location_id = None

if trail_id:  # Only create location if we have a valid trail
    try:
        # Create a location with valid trail_id
        new_location = {
            'latitude': 50.3755,
            'longitude': -4.1427,
            'sequence': 1,
            'trail_id': trail_id  # Now we have a valid trail_id
        }
        create_location_response = requests.post(
            f'{BASE_URL}/location',
            headers=headers,
            json=new_location
        )
        print("Creating location:")
        print_response(create_location_response)
        location_id = create_location_response.json().get('id')
        
        if not location_id:
            raise Exception("Failed to get location_id from response")
    except Exception as e:
        print(f"Failed to create location: {str(e)}")

    # Fix 404s by checking location_id exists
    if location_id:
        # Get specific location
        print(f"Getting location {location_id}:")
        print_response(requests.get(f'{BASE_URL}/location/{location_id}'))

        # Update location
        updated_location = {
            'latitude': 50.3756,
            'longitude': -4.1428,
            'sequence': 1,
            'trail_id': trail_id
        }
        print("Updating location:")
        print_response(requests.put(
            f'{BASE_URL}/location/{location_id}',
            headers=headers,
            json=updated_location
        ))

# 4. User Operations
print("\n=== Testing User Operations ===")
user_id = None

try:
    # Create a user
    new_user = {
        'username': USERNAME,
        'email': EMAIL,
        'password': PASSWORD
    }
    create_user_response = requests.post(
        f'{BASE_URL}/user',
        headers=headers,
        json=new_user
    )
    print("Creating user:")
    print_response(create_user_response)
    
    # Safely get user_id from response
    response_data = create_user_response.json()
    user_id = response_data.get('id')
    if not user_id:
        print("Warning: Could not get user ID from response")
except Exception as e:
    print(f"Failed to create user: {str(e)}")

# Only proceed with user operations if we have a valid user_id
if user_id:
    try:
        # Get all users
        print("Getting all users:")
        print_response(requests.get(f'{BASE_URL}/user'))

        # Get specific user
        print(f"Getting user {user_id}:")
        print_response(requests.get(f'{BASE_URL}/user/{user_id}'))

        # Update user
        updated_user = {
            'username': USERNAME,
            'email': EMAIL,
            'password': PASSWORD
        }
        print("Updating user:")
        print_response(requests.put(
            f'{BASE_URL}/user/{user_id}',
            headers=headers,
            json=updated_user
        ))
    except Exception as e:
        print(f"Failed during user operations: {str(e)}")
else:
    print("Skipping user operations due to failed user creation")

# 5. Cleanup (Delete operations)
print("\n=== Testing Delete Operations ===")

# Delete location
if location_id:
    try:
        print(f"Deleting location {location_id}:")
        print_response(requests.delete(
            f'{BASE_URL}/location/{location_id}',
            headers=headers
        ))
    except Exception as e:
        print(f"Failed to delete location: {str(e)}")

# Delete trail
if trail_id:
    try:
        print(f"Deleting trail {trail_id}:")
        print_response(requests.delete(
            f'{BASE_URL}/trail/{trail_id}',
            headers=headers
        ))
    except Exception as e:
        print(f"Failed to delete trail: {str(e)}")

# Delete user
if user_id:
    try:
        print(f"Deleting user {user_id}:")
        print_response(requests.delete(
            f'{BASE_URL}/user/{user_id}',
            headers=headers
        ))
    except Exception as e:
        print(f"Failed to delete user: {str(e)}")