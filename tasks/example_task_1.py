from locust import TaskSet, task

from endpoints.pets.pets import Pets


class GetPetsList(TaskSet):
    @task
    def get_pets_list(self):
        pets: Pets = Pets(self)

        pets.get_listPets()
