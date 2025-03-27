import requests
import uuid

ENDPOINT = "https://todo.pixegami.io/"

"""
response = requests.get(ENDPOINT)
#print(response)
data = response.json()
print(data)

status_code = response.status_code
print(status_code)
"""

"""
def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
"""


def test_can_create_task():
    """
    payload = {
        "content": "test content for tests by pytest",
        "user_id": "test_uid",
        #"task_id": "test_tid",
        "is_done": False
    }"
    """
    payload = new_task_payload()
    #create_task_response = requests.put(ENDPOINT + "/create-task", json=payload)
    create_task_response = create_task(payload)
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


def test_can_update_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "new test testing content",
        "is_done": True,
    }

    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]
    print(task_id)
    pass


def test_can_list_tasks():
    #Fn in order to list task to one user
    #Create N tasks
    N = 3
    payload = new_task_payload()
    for _ in range(N):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    user_id = payload["user_id"]
    list_tasks_response = list_tasks(user_id)
    assert list_tasks_response.status_code == 200
    data = list_tasks_response.json()

    tasks = data["tasks"]
    assert len(tasks) == N
    print("\n\n")
    print(data)


def test_can_delete_task():
    """
    - Create t
    - Delete
    - Get for check if it exists
    """
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    get_task_response = get_task(task_id)
    print("STATUS CODE!:" + str(get_task_response.status_code))
    assert get_task_response.status_code == 404
    pass


def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)


def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)


def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")


def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")


def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")


def new_task_payload():
    user_uuid = uuid.uuid4().hex
    user_id = f"test_uid_{user_uuid}"
    content = f"test_content_{uuid.uuid4().hex}"
    #print("\n\n")
    #print(f"user ID: {user_id} and content: {content}")

    return {
        "content": content,
        "user_id": user_id,
        "is_done": False
    }
