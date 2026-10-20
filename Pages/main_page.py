import os
from playwright.sync_api import Page
from dotenv import load_dotenv

load_dotenv(override=True)

admin_email = os.getenv("ADMIN_EMAIL")
admin_password = os.getenv("ADMIN_PASSWORD")
url_token = os.getenv("URL_TOKEN")
url = os.getenv("URL")


class MainPage:
    def __init__(self, page: Page, url=url, timeout=10):
        self.page = page
        self.url = url
        self.timeout = timeout
        self.email_input = page.get_by_role("textbox", name="E-mail *")
        self.password_input = page.get_by_role("textbox", name="Пароль *")
        self.login_button = page.get_by_role("button", name="Войти")
        self.allert_message = page.get_by_role("alert")

    def go_to(self, URL):
        """Открывает страницу"""
        self.page.goto(URL)

    def login(self, email: str, password: str):
        """Выполняет вход с заданными учетными данными."""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self):
        """Возвращает текст сообщения об ошибке."""
        return self.allert_message.inner_text()
