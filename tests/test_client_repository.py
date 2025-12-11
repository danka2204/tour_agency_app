import unittest
from database.client_repository import ClientRepository


class TestClientRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.repo = ClientRepository()
        cls.created_ids = []   # тут збережемо IDs створених у тесті клієнтів

    def test_create_client(self):
        new_id = self.repo.create_client("Test User", "0000000000")
        self.assertIsNotNone(new_id)
        TestClientRepository.created_ids.append(new_id)

    def test_update_client(self):
        # Створюємо тестового клієнта
        new_id = self.repo.create_client("Old Name", "1111111111")
        TestClientRepository.created_ids.append(new_id)

        # Оновлюємо
        self.repo.update_client(new_id, "New Name", "2222222222")

        # Читаємо всіх і перевіряємо
        clients = self.repo.get_all_clients()
        updated = next(c for c in clients if c["clientId"] == new_id)

        self.assertEqual(updated["clientName"], "New Name")
        self.assertEqual(updated["clientPhone"], "2222222222")

    def test_delete_client(self):
        # Створюємо тестового клієнта
        new_id = self.repo.create_client("Delete Me", "3333333333")
        TestClientRepository.created_ids.append(new_id)

        # Видаляємо
        self.repo.delete_client(new_id)

        # Перевіряємо, що його більше немає
        clients = self.repo.get_all_clients()
        exists = any(c["clientId"] == new_id for c in clients)
        self.assertFalse(exists)

    @classmethod
    def tearDownClass(cls):
        # Видаляємо тільки клієнтів, створених тестами
        for cid in cls.created_ids:
            try:
                cls.repo.delete_client(cid)
            except:
                pass  # Якщо вже видалено — ігноруємо


if __name__ == "__main__":
    unittest.main()
