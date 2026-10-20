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
postall_url = getenv('POSTAL_LINK')
login_url = getenv("LOGIN_LINK")
base_url = getenv("BASE_URL")


@allure.epic("Список Почтовые сообщения")
class TestPostallPage:

    @allure.feature("Экранная форма Почтовые сообщения")
    @allure.title("Проверка экранной формы Почтовые сообщения")
    @pytest.mark.regression
    @pytest.mark.postall_page
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_postall_page_ui_form(self,
                                  page: Page,
                                  username: str,
                                  password: str
                                  ):
        direction = DirectionMetods(page, url)
        page.set_default_timeout(60000)
        with allure.step("Переход по URL и авторизация UI"):
            direction.go_to(postall_url)
            expect(page).to_have_url(f"{login_url}")
            direction.login(username, password)
            expect(page).to_have_url(f"{postall_url}")

        with allure.step("Проверка порядка хлебных крошек"):
            breadcrumbs = page.locator(
                'fnip-breadcrumb fnip-ellipsis-hint span.clamp')
            texts = breadcrumbs.all_inner_texts()
            texts = [t.strip() for t in texts]
            expected = [
                "Единый кабинет",
                "CRM direction",
                "Почтовые сообщения"]
            assert texts == expected, f"Ожидалось: {
                expected}, Получено: {texts}"

        with allure.step("Отображение секции Письма"):
            expect(
                page.locator(
                    '[id="section-letters"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра ID"):
            expect(
                page.locator(
                    '[data-test-id="filterId"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Номер договора"):
            expect(
                page.locator(
                    '[data-test-id="filterCreditContractNumber"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра ФИО"):
            expect(
                page.locator(
                    '[data-test-id="filterPersonFullName"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Номер отслеживания"):
            expect(
                page.locator(
                    '[data-test-id="filterTrackingNumber"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Шаблон письма"):
            expect(
                page.locator(
                    '[data-test-id="filterTemplate"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Дата отправки"):
            expect(
                page.locator(
                    '[data-test-id="filterSentDate"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Дата создания"):
            expect(
                page.locator(
                    '[data-test-id="filterCreatedDate"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Дата обновления"):
            expect(
                page.locator(
                    '[data-test-id="filterUpdatedDate"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Состояние"):
            expect(
                page.locator(
                    '[data-test-id="filterState"]'
                    )).to_be_visible()
            page.locator(
                    '[data-test-id="filterState"]'
                    ).click()
            expect(
                page.locator(
                    '[data-test-id="filterState-Returned"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="filterState-Sent"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="filterState-Created"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="filterState-Delivered"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Тип письма"):
            expect(
                page.locator(
                    '[data-test-id="filterType"]'
                    )).to_be_visible()
            page.locator(
                    '[data-test-id="filterType"]'
                    ).click()
            expect(
                page.locator(
                    '[data-test-id="filterType-all"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="filterType-LetterOfDemand"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="filterType-LetterImhaPlan"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="filterType-LetterimhaFact"]'
                    )).to_be_visible()

        with allure.step("Отображение столбца Тип письма"):
            expect(
                page.locator(
                    '[col-id="type"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Дата создания/обновления"):
            expect(
                page.locator(
                    '[col-id="0"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Дата отправки"):
            expect(
                page.locator(
                    '[col-id="SentAt"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Номер договора"):
            expect(
                page.locator(
                    '[col-id="creditContractNumber"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Адрес"):
            expect(
                page.locator(
                    '[col-id="address"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Состояние"):
            expect(
                page.locator(
                    '[col-id="state"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Номер отслеживания"):
            expect(
                page.locator(
                    '[col-id="TrackingNumber"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Шаблон письма"):
            expect(
                page.locator(
                    '[col-id="template"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение кнопки Скачать"):
            expect(
                page.locator(
                    '[data-appearance="action-button"]'
                    ).nth(0)).to_be_visible()
