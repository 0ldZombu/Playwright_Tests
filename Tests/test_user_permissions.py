import pytest
import allure
from os import getenv
from dotenv import load_dotenv
from playwright.sync_api import expect
from Pages.main_page import MainPage
from Pages.data_templates import operation_codes

load_dotenv(override=True)

admin_email = getenv('ADMIN_EMAIL')
admin_password = getenv('ADMIN_PASSWORD')
urpa_email = getenv('URPA_EMAIL')
urpa_password = getenv('URPA_PASSWORD')
urpa_readonly_email = getenv('URPA_READONLY_EMAIL')
urpa_readonly_password = getenv('URPA_READONLY_PASSWORD')
surpa_email = getenv('SURPA_EMAIL')
surpa_password = getenv('SURPA_PASSWORD')
lawyer_email = getenv('LAWYER_EMAIL')
lawyer_password = getenv('LAWYER_PASSWORD')
manager_email = getenv('DIRECTIONMANAGER_EMAIL')
manager_password = getenv('DIRECTIONMANAGER_PASSWORD')
directionadmin_email = getenv('DIRECTIONADMIN_EMAIL')
directionadmin_password = getenv('DIRECTIONADMIN_PASSWORD')
url = getenv('BASE_URL')
login_url = getenv("LOGIN_LINK")


@allure.epic("CRM Direction")
@allure.feature("Проверка прав пользователей")
class TestUserPermissions:

    @allure.step("Получение permissions пользователя {username} из ответа API")
    def get_permissions_from_response(self, page, username, password):
        """Общий метод для получения permissions после логина"""
        response_data = {}

        def capture_response(response):
            if "Api/User/current/permissions" in response.url:
                nonlocal response_data
                response_data = response.json()
        page.on("response", capture_response)

        with allure.step(f"Авторизация пользователя {username}"):
            permission_page = MainPage(page)
            permission_page.go_to(url)
            expect(page).to_have_url(login_url)
            permission_page.login(username, password)
            expect(page.get_by_role(
                "heading", name="Кабинеты")).to_be_visible()
            page.wait_for_timeout(1000)

        with allure.step("Извлечение permissions из ответа"):
            permissions = response_data if isinstance(
                response_data, list) else []
            result = [
                p.get("name")
                for p in permissions
                if isinstance(p, dict) and p.get("name")
            ]
            allure.attach(
                str(result),
                name=f"Permissions для {username}",
                attachment_type=allure.attachment_type.TEXT
            )
            return result

    @allure.title("Проверка прав администратора")
    @pytest.mark.parametrize('username, password', [
        (f'{directionadmin_email}', f'{directionadmin_password}')])
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_Direction_admin_all_permissions(self, page, username, password):
        """Проверка что все operationCode из Direction_admin присутствуют"""
        with allure.step(
             f"Получение актуальных прав для пользователя {username}"):
            actual_permissions = self.get_permissions_from_response(
                page, username, password)

        with allure.step("Получение ожидаемых прав из конфигурации"):
            expected_permissions = operation_codes.get("Direction_admin", [])
            allure.attach(
                str(
                    expected_permissions
                    ), name="Ожидаемые права",
                attachment_type=allure.attachment_type.TEXT)

        with allure.step("Сравнение актуальных и ожидаемых прав"):
            missing_codes = set(expected_permissions) - set(actual_permissions)
            assert not missing_codes, f"Отсутствуют: {sorted(missing_codes)}"

    @allure.title("Проверка прав юриста")
    @pytest.mark.parametrize('username, password', [
        (f'{lawyer_email}', f'{lawyer_password}')])
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_lawyer_all_permissions(self, page, username, password):
        """Проверка что все operationCode из lawyer присутствуют"""
        with allure.step(
             f"Получение актуальных прав для пользователя {username}"):
            actual_permissions = self.get_permissions_from_response(
                page, username, password)

        with allure.step("Получение ожидаемых прав из конфигурации"):
            expected_permissions = operation_codes.get("lawyer", [])
            allure.attach(
                str(
                    expected_permissions
                    ), name="Ожидаемые права",
                attachment_type=allure.attachment_type.TEXT)

        with allure.step("Сравнение актуальных и ожидаемых прав"):
            missing_codes = set(expected_permissions) - set(actual_permissions)
            assert not missing_codes, f"Отсутствуют: {sorted(missing_codes)}"

    @allure.title("Проверка прав УРПА")
    @pytest.mark.parametrize('username, password', [
        (f'{urpa_email}', f'{urpa_password}')])
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_urpa_all_permissions(self, page, username, password):
        """Проверка что все operationCode из urpa присутствуют"""
        with allure.step(
             f"Получение актуальных прав для пользователя {username}"):
            actual_permissions = self.get_permissions_from_response(
                page, username, password)

        with allure.step("Получение ожидаемых прав из конфигурации"):
            expected_permissions = operation_codes.get("urpa", [])
            allure.attach(
                str(
                    expected_permissions
                    ), name="Ожидаемые права",
                attachment_type=allure.attachment_type.TEXT)

        with allure.step("Сравнение актуальных и ожидаемых прав"):
            missing_codes = set(expected_permissions) - set(actual_permissions)
            assert not missing_codes, f"Отсутствуют: {sorted(missing_codes)}"

    @allure.title("Проверка прав УРПА только для чтения")
    @pytest.mark.parametrize('username, password', [
        (f'{urpa_readonly_email}', f'{urpa_readonly_password}')])
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_urpa_readonly_all_permissions(self, page, username, password):
        """Проверка что все operationCode из urpa_readonly присутствуют"""
        with allure.step(
                f"Получение актуальных прав для пользователя {username}"):
            actual_permissions = self.get_permissions_from_response(
                page, username, password)

        with allure.step("Получение ожидаемых прав из конфигурации"):
            expected_permissions = operation_codes.get("urpa_readonly", [])
            allure.attach(
                str(
                    expected_permissions
                    ), name="Ожидаемые права",
                attachment_type=allure.attachment_type.TEXT)

        with allure.step("Сравнение актуальных и ожидаемых прав"):
            missing_codes = set(expected_permissions) - set(actual_permissions)
            assert not missing_codes, f"Отсутствуют: {sorted(missing_codes)}"

    @allure.title("Проверка прав супер-УРПА")
    @pytest.mark.parametrize('username, password', [
        (f'{surpa_email}', f'{surpa_password}')])
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_super_urpa_all_permissions(self, page, username, password):
        """Проверка что все operationCode из super_urpa присутствуют"""
        with allure.step(
             f"Получение актуальных прав для пользователя {username}"):
            actual_permissions = self.get_permissions_from_response(
                page, username, password)

        with allure.step("Получение ожидаемых прав из конфигурации"):
            expected_permissions = operation_codes.get("super_urpa", [])
            allure.attach(
                str(
                    expected_permissions
                    ), name="Ожидаемые права",
                attachment_type=allure.attachment_type.TEXT)

        with allure.step("Сравнение актуальных и ожидаемых прав"):
            missing_codes = set(expected_permissions) - set(actual_permissions)
            assert not missing_codes, f"Отсутствуют: {sorted(missing_codes)}"
