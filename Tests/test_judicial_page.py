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
judicial_url = getenv('JUDICIAL_LINK')
login_url = getenv("LOGIN_LINK")
base_url = getenv("BASE_URL")


@allure.epic("Список Судебные производства")
class TestJudicialPage:

    @allure.feature("Экранная форма Судебные производства")
    @allure.title("Проверка экранной формы Судебные производства")
    @pytest.mark.regression
    @pytest.mark.judicial_page
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_judicial_page_ui_form(self,
                                   page: Page,
                                   username: str,
                                   password: str
                                   ):
        collection = DirectionMetods(page, url)
        page.set_default_timeout(60000)
        with allure.step("Переход по URL и авторизация UI"):
            collection.go_to(judicial_url)
            expect(page).to_have_url(f"{login_url}")
            collection.login(username, password)
            expect(page).to_have_url(f"{judicial_url}")

        with allure.step("Проверка порядка хлебных крошек"):
            breadcrumbs = page.locator(
                'fnip-breadcrumb fnip-ellipsis-hint span.clamp')
            texts = breadcrumbs.all_inner_texts()
            texts = [t.strip() for t in texts]
            expected = [
                "Единый кабинет",
                "CRM Collection",
                "Судебные производства",
                "Все судебные производства"]
            assert texts == expected, f"Ожидалось: {
                expected}, Получено: {texts}"

        with allure.step("Отображение фильтра Номер кредитного договора"):
            expect(
                page.locator(
                    '[data-test-id="filterContractNumber"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра ФИО заемщика"):
            expect(
                page.locator(
                    '[data-test-id="filterBorrowerFullName"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Статус"):
            expect(
                page.locator(
                    '[data-test-id="filterIsActive"]'
                    )).to_be_visible()
            page.locator(
                    '[data-test-id="filterIsActive"]'
                    ).click()
            expect(
                page.locator(
                    '[data-test-id="filterIsActive-false"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="filterIsActive-true"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Тип дела"):
            expect(
                page.locator(
                    '[data-test-id="filterCaseType"]'
                    )).to_be_visible()
            page.locator(
                    '[data-test-id="filterCaseType"]'
                    ).click()
            expect(
                page.locator(
                    '[data-test-id="filterCaseType-NEI"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="filterCaseType-CourtCase"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="filterCaseType-NewOwner"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="filterCaseType-Legacy"]'
                    )).to_be_visible()

        with allure.step("Отображение столбца ID"):
            expect(
                page.locator(
                    '[col-id="Id"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Создано"):
            expect(
                page.locator(
                    '[col-id="Created"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Изменено"):
            expect(
                page.locator(
                    '[col-id="Updated"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Тип дела"):
            expect(
                page.locator(
                    '[col-id="CaseType"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Номер кредитного договора"):
            expect(
                page.locator(
                    '[col-id="ContractNumber"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца ФИО заемщика"):
            expect(
                page.locator(
                    '[col-id="BorrowerFullName"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца День просрочки"):
            expect(
                page.locator(
                    '[col-id="DaysDelayFifo"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Дата схлопывания платежей"):
            expect(
                page.locator(
                    '[col-id="WithdrawalDate"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Состояние"):
            expect(
                page.locator(
                    '[col-id="WorkflowStep"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение кнопки Скачать"):
            expect(
                page.locator(
                    '[col-id="action"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение кнопки Просмотр"):
            expect(
                page.locator(
                    '[col-id="0"]'
                    ).nth(0)).to_be_visible()
