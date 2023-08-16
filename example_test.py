from locust import HttpUser

from tasks.example_task_1 import GetPetsList
from tasks.example_task_2 import GetPetDetail


class LoadTest(HttpUser):

    tasks = {
        GetPetsList: 1,
        GetPetDetail: 2
    }
