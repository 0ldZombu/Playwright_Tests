import requests
import json
import random
import os
import pytest
from playwright.sync_api import Page
from dotenv import load_dotenv
from pprint import pprint
from .upload_migration import UploadMigrationMetods

load_dotenv(override=True)

admin_email = os.getenv("ADMIN_EMAIL")
admin_password = os.getenv("ADMIN_PASSWORD")
url_token = os.getenv("URL_TOKEN")
url = os.getenv("URL")


class DirectionMetods(UploadMigrationMetods):
    """Класс методов Direction"""
    def __init__(self, page: Page, url: str = url, timeout: int = 10):
        # Вызываем конструктор родительского класса UploadMigrationMetods
        super().__init__(page, url, timeout)
        # Добавляем специфичные для Direction атрибуты
        self.token = None
        self.contracts_data = []

    def get_token_old(self):
        """"Старое получение токена"""
        try:
            url = url_token
            headers = {
                'Content-Type': 'application/json'
                }
            json_data = {
                "email": f"{admin_email}",
                "password": f"{admin_password}"
                }
            response = requests.post(
                url, timeout=self.timeout, json=json_data, headers=headers)

            assert response.status_code == 201, \
                f"Статус код {response.status_code} не соответствует заданному"
            assert response.json() is not None
            return response.json()['data']['token']
        except AssertionError:
            return pytest.fail(
                    'Произошла ошибка при получении токена')
    # token()

    def get_token(self):
        """"Получение токена"""
        try:
            url = url_token
            headers = {
                'Content-Type': 'application/json'
                }
            json_data = {
                "username": f"{admin_email}",
                "password": f"{admin_password}"
                }
            response = requests.post(
                url, timeout=self.timeout, json=json_data, headers=headers)

            assert response.status_code == 200, \
                f"Статус код {response.status_code} не соответствует заданному"
            assert response.json() is not None
            return response.json()['accessToken']
        except AssertionError:
            return pytest.fail(
                    'Произошла ошибка при получении токена')
    # token()

    def get_tags(self, token, contractId=None):
        """"Получение списка тегов по ID договора"""
        try:
            contractId = 10603
            url = self.url+f'/api/DirectionTags/contract/{contractId}/tags'
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
                }
            response = requests.get(
                url, timeout=self.timeout, headers=headers)

            assert response.status_code == 200, \
                f"Статус код {response.status_code} не соответствует заданному"
            pprint(response.status_code)
            assert response.json() is not None
            return pprint(response.json())
        except AssertionError:
            return pytest.fail(
                    'Произошла ошибка при получении списка тегов договора')
    # get_tags()

    def get_contract(self, token, contractId=None):
        """"Получение кредитного договора по его ID в БД"""
        url = self.url+f'/api/CrmDirection/contract/{contractId}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return response.json()

    # get_contract()

    def get_contracts(self,
                      token,
                      query_params=None):
        """"Получение списка кредитных договоров
        token: Токен доступа или метод для его получения
        query_params (dict, optional): Параметры фильтрации договоров.
            Пример:
            {
                "contractNumber": "string",
                "personId": 0,
                "segmentId": 0,
                "productType": "Auto",
                "firstName": "string",
                "patronymic": "string",
                "lastName": "string",
                "passport": "string",
                "arrearsDayFrom": 0,
                "arrearsDayTo": 0,
                "arrearsSumFrom": 0,
                "arrearsSumTo": 0,
                "query": "string",
                "responsibleUserId": 0,
                "creditStartDateMin": "2026-04-20",
                "creditStartDateMax": "2026-04-20",
                "strategies": ["string"],
                "workflowStates": ["None"]
            }
        Возвращает: dict: JSON ответ с договорами"""
        url = self.url+'/api/CrmDirection/contracts'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        if query_params:
            query_string = json.dumps(query_params, ensure_ascii=False)
        else:
            query_string = '{}'  # Пустой объект как строка
        params = {
            'perPage': 100,
            'page': 1,
            'query': query_string,
            'orderBy': 'DESC',
            'fieldBy': 'Id'

        }
        response = requests.get(
            url, timeout=self.timeout, params=params, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return response.json()

    # get_contracts()

    def get_len_contracts(self, token):
        """"Получение длины списка кредитных договоров"""
        url = self.url+'/api/CrmDirection/contracts'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        items = response.json()['data']["page"]["items"]
        return items

    # get_len_contracts()

    def get_len_persons(self, token):
        """"Получение длины списка контактов"""
        url = self.url+'/api/CrmDirection/persons?perPage=47476571'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        items = response.json()['data']["page"]["items"]
        return items

    # get_len_persons()

    def get_persons(self, token):
        """"Получение списка контактов"""
        url = self.url+'/api/CrmDirection/persons?perPage=47476571'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return response.json()

    # get_persons()

    def get_person(self, token, id=None):
        """"Получение сконтакта по ID"""
        url = self.url+f'/api/CrmDirection/person/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return response.json()

    # get_persons()

    def get_client(self, token):
        """"Получение списка физ.лиц"""
        url = self.url+'/api/Client'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_client()

    def get_len_client(self, token):
        """"Получение длины списка физ.лиц"""
        url = self.url+'/api/Client'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        items = response.json()['data']["page"]["items"]
        return pprint(items)

    # get_len_client()

    def get_client_on_id(self, token):
        """"Получение физ.лица по его ID"""
        id = 16
        url = self.url+f'/api/Client/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_client_on_id()

    def get_client_activities_on_id(self, token):
        """"Получение активность физ.лица по его ID"""
        id = 2
        url = self.url+f'/api/Client/{id}/activities'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_client_activities_on_id()

    def get_coborrowers_on_id(self, token, id=None):
        """"Получение созаёмщиков по ID контракта"""
        url = self.url+f'/api/DirectionContract/{id}/coborrowers'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return response.json()

    # get_coborrowers_on_id()

    # Возвращает список вне зависимости от ID
    def get_guarantors_on_id(self, token, id=None):
        """"Получение поручителей по ID контракта"""
        url = self.url+f'/api/DirectionContract/{id}/guarantors'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return response.json()

    # get_guarantors_on_id()

    def get_comments_on_id(self, token):
        """"Получение комментариев по ID контракта"""
        id = 2
        url = self.url+f'/api/DirectionContract/{id}/comments'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_comments_on_id()

    def post_comments_on_id(self, token, random_string):
        """"Отправка комментариев по ID контракта"""
        id = 2
        url = self.url+f'/api/DirectionContract/{id}/comments'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
                        "contractId": 2,
                        "comment": f"{random_string()}"
                    }
        response = requests.post(
            url, timeout=self.timeout, json=json_data, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_comments_on_id()

    def del_comments_on_id(self, token):
        """"Удаление комментариев по ID контракта и комментария"""
        contractId = 2
        commentId = 6
        url = self.url+f'/api/DirectionContract/{
            contractId}/comments/{commentId}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.delete(
            url, timeout=self.timeout, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # del_comments_on_id()

    def get_files_on_id(self, token):
        """"Получение списка файлов по ID контракта"""
        contractId = 2
        url = self.url+f'/api/DirectionContract/{contractId}/files'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_files_on_id()

    def get_activities_on_id(self, token):
        """"Получение списка активностей по ID person"""
        personId = 1
        url = self.url+f'/api/DirectionPerson/{personId}/activities'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_activities_on_id()

    def post_activities_on_id(self, token):
        """"Создание  активностей по ID person"""
        clientId = 1
        url = self.url+f'/api/DirectionPerson/{clientId}/activities'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {}
        response = requests.post(
            url, timeout=self.timeout, json=json_data, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_activities_on_id()

    def get_phones_on_id(self, token):
        """"Получение телефона по ID"""
        id = 1
        url = self.url+f'/api/DirectionPhones/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)

        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_phones_on_id()

    def put_phones_on_id(self, token):
        """"Получение телефона по ID"""
        id = 1
        url = self.url+f'/api/DirectionPhones/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
                    "clientId": 9,
                    "comment": "labore",
                    "phoneNumber": "7777777771"
                    }
        response = requests.put(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # put_phones_on_id()

    def del_phones_on_id(self, token):
        """"Получение телефона по ID"""
        id = 1
        url = self.url+f'/api/DirectionPhones/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.delete(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # del_phones_on_id()

    def get_phones(self, token):
        """"Получение списка телефонов"""
        url = self.url+'/api/DirectionPhones'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_phones()

    def create_new_phone(self, token, random_string):
        """"Создание нового телефона"""
        url = self.url+'/api/DirectionPhones'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
                    "clientId": 1,
                    "comment": f"{random_string()}",
                    "phoneNumber": f"{random_string()}"
                    }
        response = requests.post(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # create_new_phone()

    def get_contact(self, token):
        """"Получение контакта по ID"""
        id = 1
        url = self.url+f'/api/Contact/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_contact()

    def put_contact(self, token, random_string, random_number):
        """"Изменение контакта по ID"""
        id = 1
        url = self.url+f'/api/Contact/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
                    "comment": f"{random_string()}",
                    "phoneNumber": f"{random_number()}"
                    }
        response = requests.put(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # put_contact()

    def del_contact(self, token):
        """"Удаление контакта по ID"""
        id = 1
        url = self.url+f'/api/Contact/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.put(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # del_contact()

    def post_contact(self, token, random_string, random_number):
        """"Создание контакта"""
        url = self.url+'/api/Contact'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
                    "clientId": 5,
                    "comment": f"{random_string()}",
                    "phoneNumber": f"{random_number()}"
                    }
        response = requests.post(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_contact()

    def get_guarantors(self, token):
        """"Получение поручителя по ID"""
        id = 1
        url = self.url+f'/api/Contract/{id}/guarantors'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_guarantors()

    def get_coborrowers(self, token):
        """"Получение созаёмщиков по ID"""
        id = 1
        url = self.url+f'/api/Contract/{id}/coborrowers'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_coborrowers()

    def get_payments(self, token):
        """"Получение списка платежей кред договора"""
        id = 1
        url = self.url+f'/api/CrmDirection/contract/{id}/payments'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_payments()

    def get_zalogs(self, token):
        """"Получение списка залогов кред договора"""
        id = 1
        url = self.url+f'/api/CrmDirection/contract/{id}/zalogs'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_zalogs()

    def put_contract(self, token):
        """"Изменение кред договора по ID и сегменту"""
        contractId = 3
        segmentId = 2
        url = self.url + \
            f'/api/CrmDirection/contract/{
                contractId}/segment/{segmentId}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.put(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # put_contract()

    def get_callLists(self, token):
        """"Получение списков обзвонов"""
        url = self.url+'/api/CrmDirection/callLists'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_callLists()

    def post_callLists(self, token, random_string):
        """"Создание списка обзвона"""
        url = self.url + '/api/CrmDirection/callLists'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
                    "name": f"test_callList_{random.randint(1, 1000)}",
                    "callListStateType": "Export",
                    "responsible": f"{random_string()}"
                    }
        response = requests.post(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_callLists()

    def del_callLists(self, token):
        """"Удаление списка обзвонов"""
        id = 4
        url = self.url+f'/api/CrmDirection/callLists/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.delete(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # del_callLists()

    def get_callList(self, token):
        """"Получение списка обзвонов"""
        id = 1
        url = self.url+f'/api/CrmDirection/callList/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_callList()

    def put_callList(self, token, random_number, random_string):
        """"Изменение списка обзвона"""
        id = 1
        url = self.url + f'/api/CrmDirection/callList/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
                    "id": 1,
                    "name": f"test_callList_{random_number()}",
                    "callListStateType": "Export",
                    "countActivities": 63919228,
                    "countProcessedActivities": -72830662,
                    "responsible": f"{random_string()}",
                    "created": "2018-10-14T07:27:55.534Z"
                    }
        response = requests.put(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # put_callList()

    def get_segments(self, token):
        """"Получение коллекшен сегментов"""
        url = self.url+'/api/CrmDirection/segments'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_segments()

    def post_segments(self, token):
        """"Создание коллекшен сегментов"""
        url = self.url + '/api/CrmDirection/segments'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
                    "name": "ad",
                    "sql": "dolore sint labore laborum",
                    "priorityType": "High",
                    "arrearsDayFrom": 1835357,
                    "arrearsDayTo": 69246890,
                    "arrearsSumFrom": 28733165.675056323,
                    "arrearsSumTo": 9851100.323933974,
                    "callListId": 13290444,
                    "lastResultActivityId": 56519262,
                    "isBankruptcy": True,
                    "isDeath": False,
                    "isInteractionRefusal": True,
                    "isResegmentation": False,
                    "levelId": 85489939,
                    "isTransferToDirectionAgency": True,
                    "DirectionAgencyName": "mollit elit voluptate ex est",
                    "products": [
                        "Auto",
                        "AutoPpt"
                    ]
                    }
        response = requests.post(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_segments()

    def del_segments(self, token):
        """"Удаление коллекшен сегментов"""
        id = 2
        url = self.url+f'/api/CrmDirection/segments/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.delete(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # del_segments()

    def get_segment(self, token):
        """"Получение коллекшен сегмента"""
        id = 1
        url = self.url+f'/api/CrmDirection/segment/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_segment()

    def put_segment(self, token):
        """"Изменение коллекшен сегмента"""
        id = 1
        url = self.url + f'/api/CrmDirection/segment/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
                "id": -22894577,
                "name": "exercitation irure ut",
                "sql": "sint nulla adipisicing",
                "priorityType": "Low",
                "arrearsDayFrom": 70363366,
                "arrearsDayTo": -98594129,
                "arrearsSumFrom": 72135169.977379,
                "arrearsSumTo": -34881510.527440086,
                "callListId": -33306086,
                "callList": {
                    "id": 19751623,
                    "name": "do molli",
                    "callListStateType": "New",
                    "countActivities": -34398070,
                    "countProcessedActivities": -72520214,
                    "responsible": "irure deserunt Duis sunt ",
                    "created": "2015-10-09T02:40:17.547Z"
                },
                "lastResultActivityId": 45410012,
                "lastResultActivity": {
                    "value": "<Circular reference to #/components/" +
                    "schemas/DirectionResultActivityDto detected>"
                },
                "isBankruptcy": True,
                "isDeath": True,
                "isInteractionRefusal": True,
                "isResegmentation": True,
                "levelId": 48790455,
                "level": {
                    "id": -53341037,
                    "name": "do Excepteur sed"
                },
                "isTransferToDirectionAgency": False,
                "DirectionAgencyName": "sit enim voluptate dolor",
                "products": [
                    "AutoPpt",
                    "AutoPpt"
                ]
                }
        response = requests.put(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # put_segment()

    def get_template(self, token):
        """"Получить шаблон"""
        id = 1
        url = self.url+f'/api/CrmDirection/templates/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_template()

    def put_template(self, token):
        """"Изменение шаблона"""
        id = 1
        url = self.url + f'/api/CrmDirection/templates/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
            "id": 59456653,
            "templateType": "Ivr",
            "name": "officia consectetur dolore deserunt",
            "body": "velit ",
            "soundNumber": "et"
            }
        response = requests.put(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # put_template()

    def del_template(self, token):
        """"Удалить шаблон"""
        id = 1
        url = self.url+f'/api/CrmDirection/templates/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.delete(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # del_template()

    def post_template(self, token):
        """"Создание шаблона"""
        id = 1
        url = self.url + f'/api/CrmDirection/templates/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
            "templateType": "Email",
            "name": "anim",
            "body": "in magna",
            "soundNumber": "officia"
            }
        response = requests.put(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_template()

    def get_templates(self, token):
        """"Получить шаблоны"""
        url = self.url+'/api/CrmDirection/templates'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_templates()

    def get_strategie(self, token):
        """"Получить статегию"""
        id = 1
        url = self.url+f'/api/CrmDirection/strategies/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_strategie()

    def put_strategies(self, token):
        """"Изменение стратегии"""
        id = 1
        url = self.url + f'/api/CrmDirection/strategies/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
            "id": -14588273,
            "name": "Ut commodo",
            "sql": "in voluptate officia",
            "priorityType": "Low",
            "arrearsDayFrom": -24558329,
            "arrearsDayTo": -96579414,
            "arrearsSumFrom": 82175654.695580095,
            "arrearsSumTo": 94152626.38596791,
            "callListId": -6945181,
            "callList": {
                "id": -13127802,
                "name": "in laborum sunt id",
                "callListStateType": "New",
                "countActivities": 19727848,
                "countProcessedActivities": -83636814,
                "responsible": "minim irure aute ad",
                "created": "2000-12-18T14:43:58.396Z"
            },
            "lastResultActivityId": 72437053,
            "lastResultActivity": {
                "id": 1365499,
                "name": "et voluptate consequat elit ad",
                "code": "veniam",
                "isActivated": True,
                "accessGroup": "fugiat irure",
                "holdDays": 95775071,
                "isRoutable": True,
                "routableSegmentId": -59411335,
                "routableSegment": {
                    "id": 73436099,
                    "name": "cupidatat",
                    "sql": "sed",
                    "priorityType": "Low",
                    "arrearsDayFrom": -90420193,
                    "arrearsDayTo": 91778724,
                    "arrearsSumFrom": 7838365.508188799,
                    "arrearsSumTo": -17452270.893123552,
                    "callListId": 39730128,
                    "callList": {
                        "id": -21185688,
                        "name": "magna",
                        "callListStateType": "New",
                        "countActivities": -52592580,
                        "countProcessedActivities": 61824745,
                        "responsible": "tempor deserunt esse fugiat",
                        "created": "1974-01-06T02:26:11.472Z"
                    },
                    "lastResultActivityId": 45035965,
                    "lastResultActivity": {
                        "value": "<Circular reference to #/components/" +
                        "schemas/DirectionResultActivityDto detected>"
                    },
                    "isBankruptcy": True,
                    "isDeath": True,
                    "isInteractionRefusal": False,
                    "isResegmentation": True,
                    "levelId": -35697571,
                    "level": {
                        "id": 83680671,
                        "name": "nostrud ea"
                    },
                    "isTransferToDirectionAgency": False,
                    "DirectionAgencyName": "ullamco dolore",
                    "products": [
                        "Auto",
                        "AutoPpt"
                    ]
                },
                "segmentIds": [
                    -33768080,
                    -99256165
                ],
                "segments": [
                    {
                        "id": -20182682,
                        "name": "non ex anim",
                        "sql": "dolore sit cillum occaecat",
                        "priorityType": "High",
                        "arrearsDayFrom": -47381815,
                        "arrearsDayTo": -21676405,
                        "arrearsSumFrom": -70321998.388315707,
                        "arrearsSumTo": -52691904.829138547,
                        "callListId": -87836897,
                        "callList": {
                            "id": -21025291,
                            "name": "Duis dolore nostrud cup",
                            "callListStateType": "Export",
                            "countActivities": 77853134,
                            "countProcessedActivities": 9557323,
                            "responsible": "consequat Ut deserunt",
                            "created": "1947-10-13T19:20:31.238Z"
                        },
                        "lastResultActivityId": -80583004,
                        "lastResultActivity": {
                            "value": "<Circular reference to #/components/" +
                            "schemas/DirectionResultActivityDto detected>"
                        },
                        "isBankruptcy": False,
                        "isDeath": True,
                        "isInteractionRefusal": True,
                        "isResegmentation": False,
                        "levelId": 67156740,
                        "level": {
                            "id": -59900353,
                            "name": "laborum esse"
                        },
                        "isTransferToDirectionAgency": True,
                        "DirectionAgencyName": "exercitation " +
                        "ullamco pariatur Excepteur",
                        "products": [
                            "Auto",
                            "AutoPpt"
                        ]
                    },
                    {
                        "id": 33306656,
                        "name": "nostrud exercitation dolore cupidatat",
                        "sql": "fugiat dolor occaecat no",
                        "priorityType": "Middle",
                        "arrearsDayFrom": 27948708,
                        "arrearsDayTo": 57733525,
                        "arrearsSumFrom": 99423857.966214776,
                        "arrearsSumTo": 98527408.289439082,
                        "callListId": -13436829,
                        "callList": {
                            "id": 32064556,
                            "name": "dolor nulla elit",
                            "callListStateType": "Export",
                            "countActivities": -13822268,
                            "countProcessedActivities": 28832194,
                            "responsible": "anim commodo aliqua",
                            "created": "2014-03-10T14:40:44.206Z"
                        },
                        "lastResultActivityId": -15719305,
                        "lastResultActivity": {
                            "value": "<Circular reference to #/components/" +
                            "schemas/DirectionResultActivityDto detected>"
                        },
                        "isBankruptcy": True,
                        "isDeath": True,
                        "isInteractionRefusal": True,
                        "isResegmentation": False,
                        "levelId": -87046438,
                        "level": {
                            "id": -47350148,
                            "name": "sed dolor"
                        },
                        "isTransferToDirectionAgency": True,
                        "DirectionAgencyName": "in dolore",
                        "products": [
                            "AutoPpt",
                            "Auto"
                        ]
                    }
                ]
            },
            "isActive": True,
            "resultActivityIds": [
                64026635,
                10463848
            ],
            "resultActivities": [
                {
                    "id": 33947411,
                    "name": "consectetur ad",
                    "code": "irure sit",
                    "isActivated": True,
                    "accessGroup": "eu ad",
                    "holdDays": -98210699,
                    "isRoutable": True,
                    "routableSegmentId": 40662761,
                    "routableSegment": {
                        "id": 62588935,
                        "name": "sint Excepteur ipsum",
                        "sql": "aliqua irure eu dolor",
                        "priorityType": "High",
                        "arrearsDayFrom": -17283872,
                        "arrearsDayTo": -6204682,
                        "arrearsSumFrom": -67924685.823906392,
                        "arrearsSumTo": 27508732.646588951,
                        "callListId": -26625320,
                        "callList": {
                            "id": 57219479,
                            "name": "et",
                            "callListStateType": "Export",
                            "countActivities": 46962828,
                            "countProcessedActivities": -7737118,
                            "responsible": "cillum amet sunt",
                            "created": "2005-05-04T05:45:27.271Z"
                        },
                        "lastResultActivityId": 28171439,
                        "lastResultActivity": {
                            "value": "<Circular reference to #/components/" +
                            "schemas/DirectionResultActivityDto detected>"
                        },
                        "isBankruptcy": True,
                        "isDeath": True,
                        "isInteractionRefusal": False,
                        "isResegmentation": False,
                        "levelId": -5821452,
                        "level": {
                            "id": 47809836,
                            "name": "id est commodo"
                        },
                        "isTransferToDirectionAgency": False,
                        "DirectionAgencyName": "\
                            nostrud esse fugiat voluptate",
                        "products": [
                            "Auto",
                            "AutoPpt"
                        ]
                    },
                    "segmentIds": [
                        -71810863,
                        -15097480
                    ],
                    "segments": [
                        {
                            "id": -98801200,
                            "name": "et elit exercitation",
                            "sql": "exercitation amet ex in",
                            "priorityType": "Middle",
                            "arrearsDayFrom": -50746018,
                            "arrearsDayTo": -48967935,
                            "arrearsSumFrom": 33686886.905887455,
                            "arrearsSumTo": -96567750.205705896,
                            "callListId": 78970055,
                            "callList": {
                                "id": 46770095,
                                "name": "cillum reprehenderit",
                                "callListStateType": "Export",
                                "countActivities": -36304206,
                                "countProcessedActivities": -17715792,
                                "responsible": "dolor amet aute officia",
                                "created": "2003-04-28T13:51:10.487Z"
                            },
                            "lastResultActivityId": 56904939,
                            "lastResultActivity": {
                                "value": "\
                                    <Circular reference to #/components/" +
                                "schemas/DirectionResultActivityDto detected>"
                            },
                            "isBankruptcy": False,
                            "isDeath": False,
                            "isInteractionRefusal": True,
                            "isResegmentation": False,
                            "levelId": -4925479,
                            "level": {
                                "id": -62991487,
                                "name": "in veniam"
                            },
                            "isTransferToDirectionAgency": True,
                            "DirectionAgencyName": "nos",
                            "products": [
                                "AutoPpt",
                                "Auto"
                            ]
                        },
                        {
                            "id": -35731257,
                            "name": "in in ut proid",
                            "sql": "culpa ad",
                            "priorityType": "Low",
                            "arrearsDayFrom": 5373370,
                            "arrearsDayTo": 70263227,
                            "arrearsSumFrom": -11994831.250990316,
                            "arrearsSumTo": 30569483.091049761,
                            "callListId": -31375313,
                            "callList": {
                                "id": 92226181,
                                "name": "deserunt anim consequat",
                                "callListStateType": "Export",
                                "countActivities": 10824373,
                                "countProcessedActivities": 38603625,
                                "responsible": "magna ut Lorem",
                                "created": "2001-01-21T13:35:58.144Z"
                            },
                            "lastResultActivityId": 39085528,
                            "lastResultActivity": {
                                "value": "\
                                    <Circular reference to #/components/" +
                                "schemas/DirectionResultActivityDto detected>"
                            },
                            "isBankruptcy": False,
                            "isDeath": False,
                            "isInteractionRefusal": False,
                            "isResegmentation": True,
                            "levelId": -58860045,
                            "level": {
                                "id": -14983595,
                                "name": "irure"
                            },
                            "isTransferToDirectionAgency": True,
                            "DirectionAgencyName": "mollit fugiat " +
                            "occaecat pariatur minim",
                            "products": [
                                "Auto",
                                "Auto"
                            ]
                        }
                    ]
                },
                {
                    "id": 87540058,
                    "name": "nulla",
                    "code": "nulla Duis",
                    "isActivated": True,
                    "accessGroup": "Excepteur in ex sunt",
                    "holdDays": 71551096,
                    "isRoutable": True,
                    "routableSegmentId": 54309665,
                    "routableSegment": {
                        "id": 73537607,
                        "name": "amet deserunt",
                        "sql": "velit",
                        "priorityType": "Low",
                        "arrearsDayFrom": -15294374,
                        "arrearsDayTo": -68126898,
                        "arrearsSumFrom": -49708892.328245603,
                        "arrearsSumTo": -11178858.003754273,
                        "callListId": 98419007,
                        "callList": {
                            "id": 53852141,
                            "name": "incididunt",
                            "callListStateType": "New",
                            "countActivities": 24010407,
                            "countProcessedActivities": 48625181,
                            "responsible": "aute",
                            "created": "1984-11-28T04:32:27.911Z"
                        },
                        "lastResultActivityId": -99909341,
                        "lastResultActivity": {
                            "value": "<Circular reference to #/components/" +
                            "schemas/DirectionResultActivityDto detected>"
                        },
                        "isBankruptcy": True,
                        "isDeath": False,
                        "isInteractionRefusal": False,
                        "isResegmentation": False,
                        "levelId": -26634901,
                        "level": {
                            "id": -80623847,
                            "name": "reprehenderit"
                        },
                        "isTransferToDirectionAgency": False,
                        "DirectionAgencyName": "id adipisicing velit",
                        "products": [
                            "Auto",
                            "AutoPpt"
                        ]
                    },
                    "segmentIds": [
                        19764886,
                        -98300899
                    ],
                    "segments": [
                        {
                            "id": 66002652,
                            "name": "minim labore eu elit Excepteur",
                            "sql": "aliqua ut cupidatat",
                            "priorityType": "Low",
                            "arrearsDayFrom": 56250823,
                            "arrearsDayTo": 46254440,
                            "arrearsSumFrom": -92760648.778942525,
                            "arrearsSumTo": -68755582.95451425,
                            "callListId": -15761921,
                            "callList": {
                                "id": -34577129,
                                "name": "sunt in",
                                "callListStateType": "Export",
                                "countActivities": 5470272,
                                "countProcessedActivities": -32334838,
                                "responsible": "ex aliquip",
                                "created": "1948-09-09T07:21:11.269Z"
                            },
                            "lastResultActivityId": -55792059,
                            "lastResultActivity": {
                                "value": "\
                                    <Circular reference to #/components/" +
                                "schemas/DirectionResultActivityDto detected>"
                            },
                            "isBankruptcy": True,
                            "isDeath": False,
                            "isInteractionRefusal": True,
                            "isResegmentation": False,
                            "levelId": -78992343,
                            "level": {
                                "id": 10450796,
                                "name": "aute Excepteur ex"
                            },
                            "isTransferToDirectionAgency": False,
                            "DirectionAgencyName": "aliquip ad",
                            "products": [
                                "Auto",
                                "Auto"
                            ]
                        },
                        {
                            "id": -29946309,
                            "name": "ipsum amet sint dolor pariatur",
                            "sql": "dolor fugiat anim",
                            "priorityType": "Low",
                            "arrearsDayFrom": 35868771,
                            "arrearsDayTo": -39052159,
                            "arrearsSumFrom": 67402944.911572814,
                            "arrearsSumTo": -89774654.680672854,
                            "callListId": 96327425,
                            "callList": {
                                "id": 19054757,
                                "name": "do Lorem Duis ex",
                                "callListStateType": "Export",
                                "countActivities": -22600744,
                                "countProcessedActivities": -39782256,
                                "responsible": "commodo",
                                "created": "1986-08-10T09:36:51.800Z"
                            },
                            "lastResultActivityId": -91044968,
                            "lastResultActivity": {
                                "value": "\
                                    <Circular reference to #/components/" +
                                "schemas/DirectionResultActivityDto detected>"
                            },
                            "isBankruptcy": True,
                            "isDeath": False,
                            "isInteractionRefusal": False,
                            "isResegmentation": False,
                            "levelId": -76826608,
                            "level": {
                                "id": -59854534,
                                "name": "in tempor Ut et"
                            },
                            "isTransferToDirectionAgency": False,
                            "DirectionAgencyName": "exercitation " +
                            "incididunt amet i",
                            "products": [
                                "Auto",
                                "AutoPpt"
                            ]
                        }
                    ]
                }
            ],
            "products": [
                "Auto",
                "AutoPpt"
            ],
            "templateId": 12121611,
            "template": {
                "id": -46043757,
                "templateType": "Email",
                "name": "veniam et",
                "body": "Duis laboris veniam",
                "soundNumber": "dolor proident consectetur"
            }
        }
        response = requests.put(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # put_strategies()

    def del_strategies(self, token):
        """"Удалить шаблоны"""
        id = 1
        url = self.url+f'/api/CrmDirection/strategies/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.delete(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # del_strategies()

    def get_strategies(self, token):
        """"Получить стратегии"""
        url = self.url+'/api/CrmDirection/strategies'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_strategies()

    def post_strategies(self, token):
        """"Создать стратегию"""
        url = self.url+'/api/CrmDirection/strategies'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
            "name": "labore aliquip Lorem",
            "sql": "est adipisicing tempor occaecat",
            "priorityType": "Low",
            "arrearsDayFrom": 3073897,
            "arrearsDayTo": 72319045,
            "arrearsSumFrom": 79843432.65713304,
            "arrearsSumTo": -63217992.335407525,
            "callListId": 11757767,
            "lastResultActivityId": 70017693,
            "isBankruptcy": False,
            "isDeath": False,
            "isInteractionRefusal": False,
            "isResegmentation": False,
            "isActive": False,
            "resultActivityIds": [
                6612995,
                -5102150
            ],
            "products": [
                "Auto",
                "Auto"
            ],
            "templateId": 13126034
            }
        response = requests.post(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_strategies()

    def get_resultActivities(self, token):
        """"Получить результат активности"""
        id = 1
        url = self.url+f'/api/CrmDirection/resultActivities/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_resultActivities()

    def put_resultActivities(self, token):
        """"Обновить результат активности"""
        id = 1
        url = self.url+f'/api/CrmDirection/resultActivities/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
            "id": -36292261,
            "name": "ut ",
            "code": "ad incididunt",
            "isActivated": False,
            "accessGroup": "minim veniam ut",
            "holdDays": 9040081,
            "isRoutable": True,
            "routableSegmentId": 68351176,
            "routableSegment": {
                "id": -60080519,
                "name": "ipsum minim",
                "sql": "esse eu Lorem Duis aliquip",
                "priorityType": "High",
                "arrearsDayFrom": -84707100,
                "arrearsDayTo": 8830249,
                "arrearsSumFrom": 10192802.990142941,
                "arrearsSumTo": 40560622.287825376,
                "callListId": 15965496,
                "callList": {
                    "id": 25352942,
                    "name": "eu qui ullamco sunt aliquip",
                    "callListStateType": "New",
                    "countActivities": -41000227,
                    "countProcessedActivities": 54606864,
                    "responsible": "sit do ex ipsum eiusmod",
                    "created": "1979-11-30T21:07:14.145Z"
                },
                "lastResultActivityId": 2952244,
                "lastResultActivity": {
                    "value": "<Circular reference to #/components/" +
                    "schemas/DirectionResultActivityDto detected>"
                },
                "isBankruptcy": True,
                "isDeath": True,
                "isInteractionRefusal": True,
                "isResegmentation": False,
                "levelId": -20974935,
                "level": {
                    "id": 815665,
                    "name": "fugiat commodo consequat au"
                },
                "isTransferToDirectionAgency": True,
                "DirectionAgencyName": "ut magna quis do",
                "products": [
                    "AutoPpt",
                    "AutoPpt"
                ]
            },
            "segmentIds": [
                77516293,
                43516758
            ],
            "segments": [
                {
                    "id": -45639223,
                    "name": "mollit do",
                    "sql": "nostrud velit fugiat sunt",
                    "priorityType": "Low",
                    "arrearsDayFrom": -28158219,
                    "arrearsDayTo": -89790240,
                    "arrearsSumFrom": -86269388.45097661,
                    "arrearsSumTo": 13207725.605419755,
                    "callListId": -29874508,
                    "callList": {
                        "id": -4569054,
                        "name": "labore in elit",
                        "callListStateType": "Export",
                        "countActivities": -2084462,
                        "countProcessedActivities": 48073305,
                        "responsible": "ut proi",
                        "created": "1969-03-05T22:32:13.141Z"
                    },
                    "lastResultActivityId": -77258150,
                    "lastResultActivity": {
                        "value": "<Circular reference to #/components/" +
                        "schemas/DirectionResultActivityDto detected>"
                    },
                    "isBankruptcy": False,
                    "isDeath": True,
                    "isInteractionRefusal": True,
                    "isResegmentation": True,
                    "levelId": 28288220,
                    "level": {
                        "id": -94608369,
                        "name": "Lorem adipisicing sunt"
                    },
                    "isTransferToDirectionAgency": False,
                    "DirectionAgencyName": "in",
                    "products": [
                        "AutoPpt",
                        "AutoPpt"
                    ]
                },
                {
                    "id": 28670881,
                    "name": "ad eiusmod ea",
                    "sql": "cillum id ad ullamco",
                    "priorityType": "Middle",
                    "arrearsDayFrom": 6925535,
                    "arrearsDayTo": 13697990,
                    "arrearsSumFrom": 97668576.557195574,
                    "arrearsSumTo": -20768789.549457893,
                    "callListId": -34366846,
                    "callList": {
                        "id": -27308476,
                        "name": "pariatur ad do exercitation",
                        "callListStateType": "Export",
                        "countActivities": 21208942,
                        "countProcessedActivities": -70038193,
                        "responsible": "et in",
                        "created": "1996-10-26T07:49:36.985Z"
                    },
                    "lastResultActivityId": -15129909,
                    "lastResultActivity": {
                        "value": "<Circular reference to #/components/" +
                        "schemas/DirectionResultActivityDto detected>"
                    },
                    "isBankruptcy": False,
                    "isDeath": False,
                    "isInteractionRefusal": False,
                    "isResegmentation": True,
                    "levelId": -94588475,
                    "level": {
                        "id": -81673069,
                        "name": ""
                    },
                    "isTransferToDirectionAgency": False,
                    "DirectionAgencyName": "voluptate aute",
                    "products": [
                        "Auto",
                        "Auto"
                    ]
                }
            ]
        }
        response = requests.put(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # put_resultActivities()

    def get_all_resultActivities(self, token):
        """"Получить результат активностей"""
        url = self.url+'/api/CrmDirection/resultActivities'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_all_resultActivities()

    def post_resultActivities(self, token):
        """"Создать результат активностей"""
        url = self.url+'/api/CrmDirection/resultActivities'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
            "name": "nulla minim quis commodo",
            "code": "tempor qui",
            "isActivated": True,
            "accessGroup": "nisi",
            "holdDays": 50771283,
            "isRoutable": True,
            "routableSegmentId": -45588699,
            "segmentIds": [
                -19818549,
                10836123
            ]
            }
        response = requests.post(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_resultActivities()

    def get_blackList(self, token):
        """"Получить чёрный список"""
        id = 1
        url = self.url+f'/api/CrmDirection/blackLists/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_blackList()

    def put_blackList(self, token, random_number):
        """"Обновить чёрный список"""
        id = 1
        url = self.url+f'/api/CrmDirection/blackLists/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
            "id": 1,
            "phoneNumber": f"{random_number()}"
            }
        response = requests.put(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # put_blackList()

    def del_blackList(self, token):
        """"Удалить чёрный список"""
        id = 1
        url = self.url+f'/api/CrmDirection/blackLists/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.delete(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # del_blackList()

    def get_blackLists(self, token):
        """"Получить чёрные списки"""
        url = self.url+'/api/CrmDirection/blackLists'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_blackLists()

    def post_blackList(self, token, random_number):
        """"Создать чёрный список"""
        url = self.url+'/api/CrmDirection/blackLists'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
            "phoneNumber": f"{random_number()}"
            }
        response = requests.post(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_blackList()

    def get_level(self, token):
        """"Получить уровень взыскания"""
        id = 1
        url = self.url+f'/api/CrmDirection/levels/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_level()

    def put_level(self, token):
        """"Обновить уровень взыскания"""
        id = 1
        url = self.url+f'/api/CrmDirection/levels/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
            "id": f'{id}',
            "name": "minim dolor fugiat veniam"
            }
        response = requests.put(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # put_level()

    def del_level(self, token):
        """"Удалить уровень взыскания"""
        id = 1
        url = self.url+f'/api/CrmDirection/levels/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # del_level()

    def get_levels(self, token):
        """"Получить уровени взыскания"""
        url = self.url+'/api/CrmDirection/levels'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_levels()

    def post_levels(self, token):
        """"Создать уровень взыскания"""
        url = self.url+'/api/CrmDirection/levels'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
            "name": "ullamco"
            }
        response = requests.post(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_levels()

    def get_DirectionAgencies(self, token):
        """"Получить коолекторские агенства"""
        url = self.url+'/api/CrmDirection/DirectionAgencies'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_DirectionAgencies()

    def post_SegmentForContractss(self, token):
        """"Создать уровень взыскания"""
        url = self.url+'/api/CrmDirection/setSegmentForContracts'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        file = None
        response = requests.post(
            url, timeout=self.timeout, files=file, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_SegmentForContractss()

    def post_ResultActivityForPersons(self, token):
        """"Установить результат активности физ. лиц"""
        url = self.url+'/api/CrmDirection/setResultActivityForPersons'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        file = None
        response = requests.post(
            url, timeout=self.timeout, files=file, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_ResultActivityForPersons()

    def get_courtDeal(self, token):
        """"Получить судебное производство"""
        id = 1
        url = self.url+f'/api/CrmDirection/courtDeals/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_courtDeal()

    def put_courtDeal(self, token):
        """"Обновить судебное производство"""
        id = 1
        url = self.url+f'/api/CrmDirection/courtDeals/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
            "id": 39415698,
            "status": "HaveOrder",
            "contractId": 23706424,
            "startDate": "2006-12-02T07:27:16.489Z",
            "endDate": "2014-11-06T08:04:38.110Z",
            "comment": "proident do non",
            "bank": "moll",
            "court": "aute",
            "feedMethod": "aliquip adipisicing",
            "courtSubmitDate": "2011-10-17T18:35:25.606Z",
            "number": "mollit dolor Duis",
            "contractTerminationDate": "1989-07-24T00:19:19.925Z",
            "decisionDate": "1984-12-17T22:06:08.856Z",
            "effectiveDate": "1995-03-10T00:19:09.960Z",
            "sum": -62404616.621245123,
            "approvedDuty": -91670117.131337881,
            "paymentDutyDate": "1981-04-29T14:10:26.873Z",
            "requestDate": "1972-10-15T11:18:26.399Z",
            "overdueDate": "1950-05-22T17:17:16.317Z",
            "result": "dolor aliqua in",
            "incomingNumber": "sunt anim",
            "enforcementDate": "1974-12-01T03:13:01.357Z",
            "settlementDate": "1996-04-15T11:50:04.892Z",
            "sumSettlement": 56384108.683083236,
            "decisionClaimDate": "1964-04-25T02:46:44.343Z",
            "numberPayment": "cillum aliqua officia sunt",
            "responsible": "officia culpa",
            "personId": 91020268,
            "enforcementDealId": 32079303,
            "contactId": -76867328,
            "contact": {
                "id": -22463901,
                "contactPerson": "minim ea",
                "contactType": "Borrower",
                "phoneNumber": "velit non eiusmod",
                "mobilePhoneNumber": "aliquip",
                "jobPhoneNumber": "exercitation proident ut",
                "series": "velit voluptate aliquip",
                "number": "deserunt Duis eiusmod",
                "issuedDate": "1990-04-06",
                "issuedBy": "voluptate in Duis",
                "dateOfBirth": "2009-08-17",
                "placeBirth": "sed ut labore in qui"
            }
        }
        response = requests.put(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # put_courtDeal()

    def del_courtDeal(self, token):
        """"Удалить судебное производство"""
        id = 1
        url = self.url+f'/api/CrmDirection/courtDeals/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.delete(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # del_courtDeal()

    def get_courtDeals(self, token):
        """"Получить судебные производства"""
        url = self.url+'/api/CrmDirection/courtDeals'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_courtDeals()

    def post_courtDeal(self, token):
        """"Создать судебное производство"""
        url = self.url+'/api/CrmDirection/courtDeals/'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
            "id": 39415698,
            "status": "HaveOrder",
            "contractId": 23706424,
            "startDate": "2006-12-02T07:27:16.489Z",
            "endDate": "2014-11-06T08:04:38.110Z",
            "comment": "proident do non",
            "bank": "moll",
            "court": "aute",
            "feedMethod": "aliquip adipisicing",
            "courtSubmitDate": "2011-10-17T18:35:25.606Z",
            "number": "mollit dolor Duis",
            "contractTerminationDate": "1989-07-24T00:19:19.925Z",
            "decisionDate": "1984-12-17T22:06:08.856Z",
            "effectiveDate": "1995-03-10T00:19:09.960Z",
            "sum": -62404616.621245123,
            "approvedDuty": -91670117.131337881,
            "paymentDutyDate": "1981-04-29T14:10:26.873Z",
            "requestDate": "1972-10-15T11:18:26.399Z",
            "overdueDate": "1950-05-22T17:17:16.317Z",
            "result": "dolor aliqua in",
            "incomingNumber": "sunt anim",
            "enforcementDate": "1974-12-01T03:13:01.357Z",
            "settlementDate": "1996-04-15T11:50:04.892Z",
            "sumSettlement": 56384108.683083236,
            "decisionClaimDate": "1964-04-25T02:46:44.343Z",
            "numberPayment": "cillum aliqua officia sunt",
            "responsible": "officia culpa",
            "personId": 91020268,
            "enforcementDealId": 32079303,
            "contactId": -76867328,
            "contact": {
                "id": -22463901,
                "contactPerson": "minim ea",
                "contactType": "Borrower",
                "phoneNumber": "velit non eiusmod",
                "mobilePhoneNumber": "aliquip",
                "jobPhoneNumber": "exercitation proident ut",
                "series": "velit voluptate aliquip",
                "number": "deserunt Duis eiusmod",
                "issuedDate": "1990-04-06",
                "issuedBy": "voluptate in Duis",
                "dateOfBirth": "2009-08-17",
                "placeBirth": "sed ut labore in qui"
            }
        }
        response = requests.post(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_courtDeal()

    def get_enforcementDeal(self, token):
        """"Получить исполнительное производство"""
        id = 1
        url = self.url+f'/api/CrmDirection/enforcementDeals/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_enforcementDeal()

    def put_enforcementDeal(self, token):
        """"Обновить исполнительное производство"""
        id = 1
        url = self.url+f'/api/CrmDirection/enforcementDeals/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
            "id": 91584677,
            "status": "Unknown",
            "contractId": -92502237,
            "clientId": 35200081,
            "debtId": -34471087,
            "startDate": "1953-10-22T05:21:38.582Z",
            "endDate": "2009-07-01T10:50:40.437Z",
            "comment": "ad cill",
            "bank": "Excepteur ad voluptate tempor",
            "court": "laborum magna",
            "feedMethod": "eiusmod est tempor ut",
            "courtSubmitDate": "1957-06-25T15:07:13.438Z",
            "number": "aute",
            "contractTerminationDate": "1990-01-08T11:50:10.689Z",
            "decisionDate": "1998-08-19T12:06:36.329Z",
            "effectiveDate": "2019-01-08T19:12:51.508Z",
            "sum": -42878922.357654624,
            "approvedDuty": 71247623.815545022,
            "paymentDutyDate": "2004-06-06T18:11:57.089Z",
            "requestDate": "1979-08-20T19:56:27.870Z",
            "overdueDate": "1950-02-17T18:58:59.063Z",
            "result": "voluptate culpa",
            "incomingNumber": "elit ad",
            "enforcementDate": "2022-05-15T19:03:19.389Z",
            "settlementDate": "1979-08-02T11:13:36.357Z",
            "sumSettlement": 54720279.619115293,
            "decisionClaimDate": "2001-04-15T11:42:46.439Z",
            "numberPayment": "m",
            "responsible": "nostrud proident in",
            "personId": -84206646,
            "courtDealId": 95607972,
            "contactId": -23919541,
            "contact": {
                "id": -72742283,
                "contactPerson": "velit aliqua",
                "contactType": "Coborrower",
                "phoneNumber": "culpa Ut",
                "mobilePhoneNumber": "eiusmod anim consectetur l",
                "jobPhoneNumber": "tempor ex magna",
                "series": "Ut",
                "number": "id dolore mollit esse",
                "issuedDate": "2011-10-09",
                "issuedBy": "aute incididunt proident consectetur",
                "dateOfBirth": "1977-04-30",
                "placeBirth": "elit commodo fugiat id"
            }
        }
        response = requests.put(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # put_enforcementDeal()

    def del_enforcementDeal(self, token):
        """"Удалить исполнительное производство"""
        id = 1
        url = self.url+f'/api/CrmDirection/enforcementDeals/{id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.delete(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # del_enforcementDeal()

    def get_enforcementDeals(self, token):
        """"Удалить исполнительные производства"""
        url = self.url+'/api/CrmDirection/enforcementDeals'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_enforcementDeals()

    def post_enforcementDeal(self, token):
        """"Создать исполнительное производство"""
        url = self.url+'/api/CrmDirection/enforcementDeals'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
            "id": 91584677,
            "status": "Unknown",
            "contractId": -92502237,
            "clientId": 35200081,
            "debtId": -34471087,
            "startDate": "1953-10-22T05:21:38.582Z",
            "endDate": "2009-07-01T10:50:40.437Z",
            "comment": "ad cill",
            "bank": "Excepteur ad voluptate tempor",
            "court": "laborum magna",
            "feedMethod": "eiusmod est tempor ut",
            "courtSubmitDate": "1957-06-25T15:07:13.438Z",
            "number": "aute",
            "contractTerminationDate": "1990-01-08T11:50:10.689Z",
            "decisionDate": "1998-08-19T12:06:36.329Z",
            "effectiveDate": "2019-01-08T19:12:51.508Z",
            "sum": -42878922.357654624,
            "approvedDuty": 71247623.815545022,
            "paymentDutyDate": "2004-06-06T18:11:57.089Z",
            "requestDate": "1979-08-20T19:56:27.870Z",
            "overdueDate": "1950-02-17T18:58:59.063Z",
            "result": "voluptate culpa",
            "incomingNumber": "elit ad",
            "enforcementDate": "2022-05-15T19:03:19.389Z",
            "settlementDate": "1979-08-02T11:13:36.357Z",
            "sumSettlement": 54720279.619115293,
            "decisionClaimDate": "2001-04-15T11:42:46.439Z",
            "numberPayment": "m",
            "responsible": "nostrud proident in",
            "personId": -84206646,
            "courtDealId": 95607972,
            "contactId": -23919541,
            "contact": {
                "id": -72742283,
                "contactPerson": "velit aliqua",
                "contactType": "Coborrower",
                "phoneNumber": "culpa Ut",
                "mobilePhoneNumber": "eiusmod anim consectetur l",
                "jobPhoneNumber": "tempor ex magna",
                "series": "Ut",
                "number": "id dolore mollit esse",
                "issuedDate": "2011-10-09",
                "issuedBy": "aute incididunt proident consectetur",
                "dateOfBirth": "1977-04-30",
                "placeBirth": "elit commodo fugiat id"
            }
        }
        response = requests.post(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_enforcementDeal()

    def get_contractsBySql(self, token):
        """"Получить контракты на базе SQL-запроса"""
        url = self.url+'/api/CrmDirection/contractsBySql'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_contractsBySql()

    def post_uploadMigration(self, token=None,
                             person_id=None,
                             override_contract=False,
                             override_person=False,
                             guarantors=False,
                             override_guarantors=False,
                             coborrowers=False,
                             override_coborrowers=False,
                             have_security=True,
                             credit_id=None):
        """"Загрузить миграцию"""
        try:
            url = self.url+'/api/CrmDirection/uploadMigration'
            headers = {
                'Authorization': f'Bearer {token}',
                'Accept': 'text/plain'
                }
            csv_filename = 'data.csv'
            number_contract, credit_id = self.create_csv_file(
                person_id=person_id,
                override_contract=override_contract,
                override_person=override_person,
                guarantors=guarantors,
                override_guarantors=override_guarantors,
                coborrowers=coborrowers,
                override_coborrowers=override_coborrowers,
                have_security=have_security,
                credit_id=credit_id)
            with open(csv_filename, 'rb') as f:
                files = {
                    'file': (csv_filename, f, 'text/csv')
                }
                response = requests.post(
                    url, timeout=self.timeout, files=files, headers=headers)
            assert response.status_code == 200, \
                f"Статус код {response.status_code} не соответствует заданному"
            assert response.json() is not None
            assert response.json()['success'] is True
            return number_contract, credit_id
        except AssertionError as e:
            return pytest.fail(
                    f'Произошла ошибка при импорте файла {str(e)}')

    # post_uploadMigration()

    def post_uploadMigration_negative(self, token):
        """"Загрузить миграцию"""
        try:
            url = self.url+'/api/CrmDirection/uploadMigration'
            headers = {
                'Authorization': f'Bearer {token}',
                'Accept': 'text/plain'
                }
            csv_filename = 'data.csv'
            with open(csv_filename, 'rb') as f:
                files = {
                    'file': (csv_filename, f, 'text/csv')
                }
                response = requests.post(
                    url, timeout=self.timeout, files=files, headers=headers)
            assert response.status_code == 200, \
                f"Статус код {response.status_code} не соответствует заданному"
            assert response.json() is not None
            assert response.json()['success'] is True
        except AssertionError:
            return pytest.fail(
                    'Произошла ошибка при импорте файла')

    def post_uploadPayments(self, token):
        """"Загрузить миграцию"""
        url = self.url+'/api/CrmDirection/uploadPayments'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        file = None
        response = requests.post(
            url, timeout=self.timeout, files=file, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_uploadPayments()

    def post_calcSegment(self, token):
        """"Загрузить миграцию"""
        url = self.url+'/api/CrmDirection/uploadPayments'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        file = None
        response = requests.post(
            url, timeout=self.timeout, files=file, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_calcSegment()

    def get_JudicialWork(self,
                         token,
                         filtr=None,
                         value=None):
        """"Получить список КД, по которым идет юридическая работа"""
        query = ''
        if filtr is not None and value is not None:
            query = f'?{filtr}={value}'
        url = self.url+'/api/JudicialWork' + f'{query}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return response.json()

    # get_JudicialWork()

    def post_JudicialWork(self, token, contractId):
        """"Загрузить миграцию"""
        url = self.url+'/api/JudicialWork'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
            "contractId": f'{contractId}',
            "caseType": "NEI"
            }
        response = requests.post(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return response.json()["data"]["id"]

    # post_JudicialWork()

    def get_Outsourcing_start_file(self, token):
        """"Получить csv файл с получениями в работу"""
        url = self.url+'/api/Outsourcing/start/file'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        # assert response.json() is not None
        return pprint(response.text)

    # get_Outsourcing_start_file()

    def get_Outsourcing_start(self, token):
        """"Получить получение в работу"""
        url = self.url+'/api/Outsourcing/start'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_Outsourcing_start()

    def get_Outsourcing_cancel_file(self, token):
        """"Получить csv файл с получениями в работу"""
        url = self.url+'/api/Outsourcing/cancel/file'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        # assert response.json() is not None
        return pprint(response.text)

    # get_Outsourcing_cancel_file()

    def get_Outsourcing_cancel(self, token):
        """"Получить отзывы из работы"""
        url = self.url+'/api/Outsourcing/cancel'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_Outsourcing_cancel()

    def get_Outsourcing_payments_file(self, token):
        """"Получить csv файл гашения по переданным \
            договорам в период нахождения актива в работе"""
        url = self.url+'/api/Outsourcing/payments/file'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        # assert response.json() is not None
        return pprint(response.text)

    # get_Outsourcing_payments_file()

    def get_Outsourcing_payments(self, token):
        """"Получить гашения по переданным \
            договорам в период нахождения актива в работе"""
        url = self.url+'/api/Outsourcing/payments'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_Outsourcing_payments()

    def get_Outsourcing_update_file(self, token):
        """"Получить csv файл обновление сумм задолженности"""
        url = self.url+'/api/Outsourcing/update/file'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        # assert response.json() is not None
        return pprint(response.text)

    # get_Outsourcing_update_file()

    def get_Outsourcing_update(self, token):
        """"Получить обновление сумм задолженности"""
        url = self.url+'/api/Outsourcing/update'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_Outsourcing_update()

    def post_calls_check(self, token):
        """"Проверяет на корректность файл \
            calls переданный от коллекторов, на соответствии колонкам"""
        url = self.url+'/api/Outsourcing/calls/check'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        file = None
        response = requests.post(
            url, timeout=self.timeout, files=file, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_calls_check()

    def post_calls(self, token):
        """"Загрузить файл с иноформацией о звонках и \
            комментариях по взаимодействию с должником по телефону"""
        url = self.url+'/api/Outsourcing/calls'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        file = None
        response = requests.post(
            url, timeout=self.timeout, files=file, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_calls()

    def post_departures_check(self, token):
        """"Проверяет на корректность файл departures переданный \
            от коллекторов, на соответствии колонкам"""
        url = self.url+'/api/Outsourcing/departures/check'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        file = None
        response = requests.post(
            url, timeout=self.timeout, files=file, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_departures_check()

    def post_departures(self, token):
        """"Загрузить файл с информацией по выездам и \
            комментариям по взаимодействию с должником"""
        url = self.url+'/api/Outsourcing/departures'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        file = None
        response = requests.post(
            url, timeout=self.timeout, files=file, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_departures()

    def post_drz_check(self, token):
        """"Проверяет на корректность файл drz переданный \
            от коллекторов, на соответствии колонкам"""
        url = self.url+'/api/Outsourcing/drz/check'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        file = None
        response = requests.post(
            url, timeout=self.timeout, files=file, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_drz_check()

    def post_drz(self, token):
        """"Загрузить файл с информацией по работе с \
            залогом (поиск/изъятие/реализация/место хранения залога и пр)"""
        url = self.url+'/api/Outsourcing/drz'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        file = None
        response = requests.post(
            url, timeout=self.timeout, files=file, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_drz()

    def get_drz(self, token):
        """"Получить историю приемов/передач договоров в/из аутсорсинг(а)"""
        url = self.url+'/api/Outsourcing/drz'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_drz()

    def get_bp_request(self, token):
        """"Получить историю приемов/передач договоров в/из аутсорсинг(а)"""
        url = self.url+'/api/Outsourcing/bp_request'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_bp_request()

    def get_files(self,
                  token,
                  ka=None,
                  name=None,
                  fileType=None,
                  createdFrom=None,
                  createdTo=None,
                  page=None,
                  perPage=None):
        """"Получить файлы агентств"""
        url = self.url+'/api/Outsourcing/files'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'ka': f'{ka}',
            'name': f'{name}',
            'fileType': f'{fileType}',
            'createdFrom': f'{createdFrom}',
            'createdTo': f'{createdTo}',
            'page': f'{page}',
            'perPage': f'{perPage}'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return response.json()

    # get_files()

    def get_file(self, token):
        """"Получить файл аутсорсинга"""
        fileId = 1
        url = self.url+f'/api/Outsourcing/file/{fileId}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_file()

    def get_personsCallListForDirectionExport(self, token):
        """"Получить список физлиц для списка обзвона (CRM Direction)"""
        url = self.url+'/api/Report/personsCallListForDirectionExport'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_personsCallListForDirectionExport()

    def post_applicationsForDirectionImport(self, token):
        """"Импорт данных по заявкам (CRM Direction)"""
        url = self.url+'/api/Report/applicationsForDirectionImport'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        file = None
        response = requests.post(
            url, timeout=self.timeout, files=file, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_applicationsForDirectionImport()

    def get_contractsForDirectionExport(self, token=None):
        """"Получить экспорт в excel \
            списка кредитных договоров (CRM Direction)"""
        url = self.url+'/api/Report/contractsForDirectionExport'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.get(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_contractsForDirectionExport()

    def post_requestDirectionCreateReport(self, token):
        """"Cоздать запрос на генерацию отчета"""
        reportType = 1
        url = self.url+f'/api/Report/requestDirectionCreateReport/{
            reportType}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        json_data = {
            "from": "1972-03-17T08:15:28.697Z",
            "to": "1981-02-24T21:12:55.345Z"
            }
        response = requests.post(
            url, timeout=self.timeout, json=json_data, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # post_requestDirectionCreateReport()\

    def get_requestDirectionReport(self, token):
        """"Получить задачу генерации отчета в Direction"""
        taskId = 1
        url = self.url+f'/api/Report/requestDirectionReport/{taskId}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.post(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_requestDirectionReport()

    def get_requestDirectionReportFile(self, token):
        """"Получить отчет по id задачи генерации отчета в Direction"""
        taskId = 1
        url = self.url+f'/api/Report/requestDirectionReport/{taskId}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.post(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_requestDirectionReportFile()\

    def get_requestDirectionReportHistory(self, token):
        """"Получить историю генераций отчетов в Direction"""
        url = self.url+'/api/Report/requestDirectionReportHistory'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.post(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_requestDirectionReportHistory()

    def get_Direction_strategy(self, token):
        """"Получить историю генераций отчетов в Direction"""
        url = self.url+'/api/DirectionStrategy/Direction-strategy'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.post(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return pprint(response.json())

    # get_Direction_strategy()

    def start_workflow_contract(self,
                                token,
                                contractId=None,
                                loanDate=None,
                                overdueDate=None):
        """"Запуск процесса по контракту"""
        query = ''
        if None not in (contractId, loanDate, overdueDate):
            query = (f'?contractId={contractId}' +
                     f'&loanDate={loanDate}&overdueDate={overdueDate}')
        url = self.url+'/api/Workflow/contract/start' + f'{query}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.post(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        # assert response.json() is not None

    def start_workflow_nei(self,
                           token,
                           contractId,
                           neiId):
        """"Запуск процесса по ИНН"""
        query = ''
        if contractId is not None and neiId is not None:
            query = f'?contractId={contractId}&neiId={neiId}'
        url = self.url+'/api/Workflow/nei/start' + f'{query}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.post(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        # assert response.json() is not None

    def get_strategy_log(self,
                         token,
                         contractId):
        """"Вернуть историю стратегий"""
        url = self.url+f'/api/DirectionContract/{contractId}/StrategyLog'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
            }
        response = requests.post(
            url, timeout=self.timeout, headers=headers)
        assert response.status_code == 200, \
            f"Статус код {response.status_code} не соответствует заданному"
        assert response.json() is not None
        return response.json()
