from locust import HttpUser, task, between
import random

class TaskUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def create_task(self):
        self.client.post('/tasks', json={
            'title': f'{random.randint(0, 9999)}',
            'status': 'в работе',
            'priority': random.randint(1,5)
        })

    @task
    def list_tasks(self):
        self.client.get('/tasks')