import requests

ENDPOINT = "https://todo.pixegami.io/"

"""
response = requests.get(ENDPOINT)
#print(response)
data = response.json()
print(data)

status_code = response.status_code
print(status_code)
"""
def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_task():
    payload = {
        "content": "test content for tests by pytest",
        "user_id": "test_uid",
        #"task_id": "test_tid",
        "is_done": False
    }
    create_task_response = requests.put(ENDPOINT + "/create-task", json=payload)
    assert create_task_response.status_code == 200

    data = create_task_response.json()
    print("\n\n")
    print(data)

    task_id = data["task"]["task_id"]
    get_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}")

    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]
    print("\n\n")
    print(get_task_data)