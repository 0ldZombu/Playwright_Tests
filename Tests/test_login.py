import pytest
import allure
from os import getenv
from dotenv import load_dotenv
from playwright.sync_api import expect, Page
from Pages.main_page import MainPage


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
url = getenv('LOGIN_LINK')


@allure.epic("Авторизация")
@allure.feature("Логин в систему")
class TestLoginPage:

    @allure.title("Авторизация под: {username}")
    @allure.description(
        "Тест проверяет успешный вход в систему для разных пользователей")
    @pytest.mark.parametrize('username, password', [
        (f'{admin_email}', f'{admin_password}'),
        (f'{urpa_email}', f'{urpa_password}'),
        (f'{urpa_readonly_email}', f'{urpa_readonly_password}'),
        (f'{surpa_email}', f'{surpa_password}'),
        (f'{lawyer_email}', f'{lawyer_password}'),
        (f'{manager_email}', f'{manager_password}'),
        (f'{directionadmin_email}', f'{directionadmin_password}'),
    ])
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login(self,
                   page: Page,
                   username: str,
                   password: str):
        with allure.step("Переход на страницу логина"):
            login_page = MainPage(page)
            login_page.go_to(url)
            expect(page).to_have_url(url)

        with allure.step(f"Выполнение входа для пользователя: {username}"):
            login_page.login(username, password)

        with allure.step("Проверка отображения" +
                         " кабинетов после успешного входа"):
            expect(page.get_by_role("heading", name="Кабинеты"),
                   "Кабинеты не отображается на странице").to_be_visible()

    @allure.title("Негативный тест логина")
    @allure.description("Тест проверяет валидацию" +
                        " полей email и пароля при входе")
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_negative(self,
                            page: Page
                            ):
        with allure.step("Переход на страницу логина"):
            login_page = MainPage(page)
            login_page.go_to(url)
            expect(page).to_have_url(url)

        with allure.step("Заполнение поля email" +
                         " некорректным значением '1231'"):
            email_field = page.locator("input#login")
            email_field.click()
            email_field.fill("1231")
            page.get_by_role("heading", name="Вход").click()
            expect(page.get_by_text(
                "Укажите корректный email"),
                "Валидация пароля прошла").to_be_visible()

        with allure.step("Заполнение поля password" +
                         " значением '123' (нет символов верхнего регистра)"):
            password_field = page.locator("input#password")
            password_field.click()
            password_field.fill("123")
            page.get_by_role("heading", name="Вход").click()
            expect(page.get_by_text(
                "Пароль должен содержать символы верхнего регистра!"),
                "Валидация пароля прошла").to_be_visible()

        with allure.step("Заполнение поля password" +
                         " значением '123QW' (нет символов нижнего регистра)"):
            page.get_by_role("heading", name="Вход").click()
            password_field.click()
            password_field.fill("123QW")
            page.get_by_role("heading", name="Вход").click()
            expect(page.get_by_text(
                "Пароль должен содержать символы нижнего регистра!"),
                "Валидация пароля прошла").to_be_visible()

        with allure.step("Заполнение поля password" +
                         " значением '123QWa' (валидный пароль)"):
            password_field.click()
            password_field.fill("123QWa")
            page.locator("fnip-button").filter(has_text="Войти").click()

        with allure.step("Заполнение поля email" +
                         " значением '1231@qwe.ru' (некорректный email)"):
            email_field.click()
            email_field.fill("1231@qwe.ru")
            page.get_by_role("heading", name="Вход").click()
            expect(page.get_by_text(
                "Укажите корректный email"),
                "Валидация почты прошла").to_be_hidden()

        with allure.step("Попытка входа с некорректными данными"):
            page.get_by_role("button", name="Войти").click()
            expect(page.get_by_role("alert"),
                   "Алерт не появился").to_be_visible()
