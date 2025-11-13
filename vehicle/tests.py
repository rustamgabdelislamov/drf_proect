from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User

class VehicleTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(username='admin', password='1990')

    def test_create_car(self):
        """ Тестирование создания машины """

        # Добавляем аутентификацию
        self.client.force_authenticate(user=self.user)

        data = {
            'title': "Test",
            'description': "Автомобиль",
            'milage': [{
                'milage': 0,
                'year': 2025
            }]
        }
        response = self.client.post(
            '/cars/',
            data=data,
            format='json' # Явно указываем формат данных
        )
        response_data = response.json()
        print("Response:", response_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['title'], 'Test')
        self.assertEqual(response_data['description'], 'Автомобиль')
        self.assertEqual(len(response_data['milage']), 1)  # Проверяем, что пробег создан
        self.assertEqual(response_data['milage'][0]['milage'], 0)
