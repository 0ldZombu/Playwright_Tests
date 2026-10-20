import pytest
import allure
from os import getenv
from dotenv import load_dotenv
from playwright.sync_api import expect, Page
from Pages.direction_metods import DirectionMetods


load_dotenv(override=True)

admin_email = getenv('ADMIN_EMAIL')
admin_password = getenv('ADMIN_PASSWORD')
url = getenv('URL')
reports_url = getenv('REPORT_LINK')
login_url = getenv("LOGIN_LINK")
base_url = getenv("BASE_URL")


@allure.epic("Список Отчёты")
class TestReportPage:

    @allure.feature("Экранная форма Сформированные отчёты")
    @allure.title("Проверка экранной формы Сформированные отчёты")
    @pytest.mark.regression
    @pytest.mark.report_page
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_report_page_ui_form(self,
                                 page: Page,
                                 username: str,
                                 password: str
                                 ):
        direction = DirectionMetods(page, url)
        page.set_default_timeout(60000)
        with allure.step("Переход по URL и авторизация UI"):
            direction.go_to(reports_url)
            expect(page).to_have_url(f"{login_url}")
            direction.login(username, password)
            expect(page).to_have_url(f"{reports_url}")

        with allure.step("Проверка порядка хлебных крошек"):
            breadcrumbs = page.locator(
                'fnip-breadcrumb fnip-ellipsis-hint span.clamp')
            texts = breadcrumbs.all_inner_texts()
            texts = [t.strip() for t in texts]
            expected = [
                "Единый кабинет",
                "CRM direction",
                "Журнал отчётов"]
            assert texts == expected, f"Ожидалось: {
                expected}, Получено: {texts}"

        with allure.step("Отображение Сформировать отчёт"):
            expect(
                page.locator(
                    '[data-test-label="Сформировать отчёт"]'
                    )).to_be_visible()

        with allure.step("Отображение Всё"):
            expect(
                page.locator(
                    '[label="Все"]'
                    )).to_be_visible()

        with allure.step("Отображение Общий отчет по direction"):
            expect(
                page.get_by_text("Общий отчет по direction").nth(0)
                ).to_be_visible()

        with allure.step("Отображение Отчет по последним активностям"):
            expect(
                page.get_by_text("Отчет по последним активностям")
                ).to_be_visible()

        with allure.step("Отображение Отчет об исключении или изменении залога"
                         ):
            expect(
                page.get_by_text("Отчет об исключении или изменении залога")
                ).to_be_visible()

        with allure.step("Отображение Отчет по КД в аутсорсе"):
            expect(
                page.get_by_text("Отчет по КД в аутсорсе")
                ).to_be_visible()

        with allure.step("Отображение Отчет Легал"):
            expect(
                page.get_by_text("Отчет Легал")
                ).to_be_visible()

        with allure.step("Отображение Отчет по 60+"):
            expect(
                page.get_by_text("Отчет по 60+").nth(0)
                ).to_be_visible()

        with allure.step("Отображение Отчет по 90+"):
            expect(
                page.get_by_text("Отчет по 90+").nth(0)
                ).to_be_visible()

    @allure.feature("Экранная форма Сформировать отчёт")
    @allure.title("Проверка экранной формы Сформировать отчёт")
    @pytest.mark.regression
    @pytest.mark.report_page
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_report_new_page_ui_form(self,
                                     page: Page,
                                     username: str,
                                     password: str
                                     ):
        direction = DirectionMetods(page, url)
        page.set_default_timeout(60000)
        with allure.step("Переход по URL и авторизация UI"):
            direction.go_to(reports_url)
            expect(page).to_have_url(f"{login_url}")
            direction.login(username, password)
            expect(page).to_have_url(f"{reports_url}")

        with allure.step("Проверка порядка хлебных крошек"):
            breadcrumbs = page.locator(
                'fnip-breadcrumb fnip-ellipsis-hint span.clamp')
            texts = breadcrumbs.all_inner_texts()
            texts = [t.strip() for t in texts]
            expected = [
                "Единый кабинет",
                "CRM direction",
                "Журнал отчётов"]
            assert texts == expected, f"Ожидалось: {
                expected}, Получено: {texts}"

        with allure.step("Отображение Сформировать отчёт"):
            expect(
                page.locator(
                    '[data-test-label="Сформировать отчёт"]'
                    )).to_be_visible()
            page.locator(
                    '[data-test-label="Сформировать отчёт"]'
                    ).click()

        with allure.step("Отображение Общий отчет по direction"):
            expect(
                page.get_by_text("Общий отчет по direction").nth(0)
                ).to_be_visible()

        with allure.step("Отображение Отчет по последним активностям"):
            expect(
                page.get_by_text("Отчет по последним активностям")
                ).to_be_visible()

        with allure.step("Отображение Отчет об исключении или изменении залога"
                         ):
            expect(
                page.get_by_text("Отчет об исключении или изменении залога")
                ).to_be_visible()

        with allure.step("Отображение Отчет по КД в аутсорсе"):
            expect(
                page.get_by_text("Отчет по КД в аутсорсе")
                ).to_be_visible()

        with allure.step("Отображение Отчет Легал"):
            expect(
                page.get_by_text("Отчет Легал")
                ).to_be_visible()

        with allure.step("Отображение Отчет по 60+"):
            expect(
                page.get_by_text("Отчет по 60+").nth(0)
                ).to_be_visible()

        with allure.step("Отображение Отчет по 90+"):
            expect(
                page.get_by_text("Отчет по 90+").nth(0)
                ).to_be_visible()
