from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestAmenities(APITestCase):

    NAME = "Amenity Test"
    DES = "Amenity Test Description"

    URL = "/api/v1/rooms/amenities/"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DES,
        )

    def test_all_amenities(self):

        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 200, "Status Code not 200")

        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.NAME)

    def test_create_amenity(self):

        new_amenity_name = "New"
        new_amenity_description = "hahaha"
        response = self.client.post(
            self.URL,
            data={"name": new_amenity_name, "description": new_amenity_description},
        )
        data = response.json()

        self.assertEqual(response.status_code, 200, "Not 200 status code")

        self.assertEqual(data["name"], new_amenity_name)

        self.assertEqual(data["description"], new_amenity_description)

        response = self.client.post(self.URL)


class TestAmenity(APITestCase):

    NAME = "Amenity Test"
    DES = "Amenity Test Description"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DES,
        )

    def test_get_amenity(self):

        response = self.client.get("/api/v1/rooms/amenities/2")

        self.assertEqual(response.status_code, 404)

        response = self.client.get("/api/v1/rooms/amenities/1")

        self.assertEqual(response.status_code, 200)


class TestRooms(APITestCase):

    def setUp(self):
        user = User.objects.create(username="test")
        user.set_password("1234")
        user.save()

        self.user = user

    def test_create_room(self):

        self.client.force_login(self.user)

        response = self.client.post("/api/v1/rooms/")

        print(response)
