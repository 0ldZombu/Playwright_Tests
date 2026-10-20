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
outsource_url = getenv('OUTSOURS_LINK')
files_from_ka_url = getenv('FILES_FROM_KA_LINK')
files_to_ka_url = getenv('FILES_TO_KA_LINK')
login_url = getenv("LOGIN_LINK")
base_url = getenv("BASE_URL")


@allure.epic("Кабинет Аутсорс")
class TestOutsoursePage:

    @allure.feature("Экранная форма Аутсорс")
    @allure.title("Проверка экранной формы Аутсорс")
    @pytest.mark.regression
    @pytest.mark.outsource_page
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_outsource_page_ui_form(self,
                                    page: Page,
                                    username: str,
                                    password: str
                                    ):
        direction = DirectionMetods(page, url)
        page.set_default_timeout(60000)
        with allure.step("Переход по URL и авторизация UI"):
            direction.go_to(outsource_url)
            expect(page).to_have_url(f"{login_url}")
            direction.login(username, password)
            expect(page).to_have_url(f"{outsource_url}")

        with allure.step("Проверка порядка хлебных крошек"):
            breadcrumbs = page.locator(
                'fnip-breadcrumb fnip-ellipsis-hint span.clamp')
            texts = breadcrumbs.all_inner_texts()
            texts = [t.strip() for t in texts]
            expected = [
                "Единый кабинет",
                "CRM direction",
                "Аутсорс",
                "Кредитные договора"]
            assert texts == expected, f"Ожидалось: {
                expected}, Получено: {texts}"

        with allure.step("Отображение Кредитные договора"):
            expect(
                page.locator(
                    '[header="Кредитные договора"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Номер кредитного договора(-ов)"):
            expect(
                page.locator(
                    '[fieldid="contractNumbers"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра КА"):
            expect(
                page.locator(
                    '[fieldid="ka"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Дата передачи в КА"):
            expect(
                page.locator(
                    '[fieldid="startDate"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра В КА Сегодня"):
            expect(
                page.locator(
                    '[data-test-id="startDateSelect-0"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра В КА Неделя"):
            expect(
                page.locator(
                    '[data-test-id="startDateSelect-1"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра В КА Месяц"):
            expect(
                page.locator(
                    '[data-test-id="startDateSelect-2"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Дата отзыва из КА"):
            expect(
                page.locator(
                    '[fieldid="cancelDate"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра из КА Сегодня"):
            expect(
                page.locator(
                    '[data-test-id="cancelDateSelect"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра из КА Неделя"):
            expect(
                page.locator(
                    '[data-test-id="cancelDateSelect-1"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра из КА Месяц"):
            expect(
                page.locator(
                    '[data-test-id="cancelDateSelect-2"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Статус"):
            expect(
                page.locator(
                    '[data-test-id="statusCode"]'
                    )).to_be_visible()
            page.locator(
                    '[data-test-id="statusCode"]'
                    ).click()
            expect(
                page.locator(
                    '[data-test-id="statusCode-None"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="statusCode-Payout"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="statusCode-Expired"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="statusCode-Force"]'
                    )).to_be_visible()

        with allure.step("Отображение Столбца ID"):
            expect(
                page.locator(
                    '[col-id="contractId"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение Столбца Номер кредитного договора"):
            expect(
                page.locator(
                    '[col-id="creditContractNumber"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение Столбца Банк"):
            expect(
                page.locator(
                    '[col-id="bank"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение Столбца КА"):
            expect(
                page.locator(
                    '[col-id="ka"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение Столбца Стратегия"):
            expect(
                page.locator(
                    '[col-id="strategy"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение Столбца Дата передачи в КА"):
            expect(
                page.locator(
                    '[col-id="sentToKa"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение Столбца Дата отзыва из КА"):
            expect(
                page.locator(
                    '[col-id="recalledFromKA"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение Столбца Состояние"):
            expect(
                page.locator(
                    '[col-id="currentStatus"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение Столбца Статус"):
            expect(
                page.locator(
                    '[col-id="statusInfo"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение Столбца Комментарий к отзыву"):
            expect(
                page.locator(
                    '[col-id="comment"]'
                    ).nth(0)).to_be_visible()


@allure.epic("Кабинет Аутсорс")
class TestFilesFromKaPage:

    @allure.feature("Экранная форма Файлы от КА")
    @allure.title("Проверка экранной формы от КА")
    @pytest.mark.regression
    @pytest.mark.files_to_ka_page
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_files_from_ka_ui_form(self,
                                   page: Page,
                                   username: str,
                                   password: str
                                   ):
        direction = DirectionMetods(page, url)
        page.set_default_timeout(60000)
        with allure.step("Переход по URL и авторизация UI"):
            direction.go_to(files_from_ka_url)
            expect(page).to_have_url(f"{login_url}")
            direction.login(username, password)
            expect(page).to_have_url(f"{files_from_ka_url}")

        with allure.step("Проверка порядка хлебных крошек"):
            breadcrumbs = page.locator(
                'fnip-breadcrumb fnip-ellipsis-hint span.clamp')
            texts = breadcrumbs.all_inner_texts()
            texts = [t.strip() for t in texts]
            expected = [
                "Единый кабинет",
                "CRM direction",
                "Аутсорс",
                "Файлы от КА"]
            assert texts == expected, f"Ожидалось: {
                expected}, Получено: {texts}"

        with allure.step("Отображение Файлы от КА"):
            expect(
                page.locator(
                    '[header="Файлы от КА"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра КА"):
            expect(
                page.locator(
                    '[id="ka"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Название"):
            expect(
                page.locator(
                    '[id="name"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Создано"):
            expect(
                page.locator(
                    '[id="created"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Сегодня"):
            expect(
                page.locator(
                    '[data-test-id="createdSelect-0"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Неделя"):
            expect(
                page.locator(
                    '[data-test-id="createdSelect-1"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Месяц"):
            expect(
                page.locator(
                    '[data-test-id="createdSelect-2"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Тип файла"):
            expect(
                page.locator(
                    '[fieldid="fileType"]'
                    )).to_be_visible()


@allure.epic("Кабинет Аутсорс")
class TestFilesToKaPage:

    @allure.feature("Экранная форма Файлы для КА")
    @allure.title("Проверка экранной формы для КА")
    @pytest.mark.regression
    @pytest.mark.files_from_ka_page
    @pytest.mark.test_test
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_files_to_ka_ui_form(self,
                                 page: Page,
                                 username: str,
                                 password: str
                                 ):
        direction = DirectionMetods(page, url)
        page.set_default_timeout(60000)
        with allure.step("Переход по URL и авторизация UI"):
            direction.go_to(files_to_ka_url)
            expect(page).to_have_url(f"{login_url}")
            direction.login(username, password)
            expect(page).to_have_url(f"{files_to_ka_url}")

        with allure.step("Проверка порядка хлебных крошек"):
            breadcrumbs = page.locator(
                'fnip-breadcrumb fnip-ellipsis-hint span.clamp')
            texts = breadcrumbs.all_inner_texts()
            texts = [t.strip() for t in texts]
            expected = [
                "Единый кабинет",
                "CRM direction",
                "Аутсорс",
                "Файлы для КА"]
            assert texts == expected, f"Ожидалось: {
                expected}, Получено: {texts}"

        with allure.step("Отображение Файлы для КА"):
            expect(
                page.locator(
                    '[header="Файлы для КА"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра КА"):
            expect(
                page.locator(
                    '[id="ka"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Название"):
            expect(
                page.locator(
                    '[id="name"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Создано"):
            expect(
                page.locator(
                    '[id="created"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Сегодня"):
            expect(
                page.locator(
                    '[data-test-id="createdSelect-0"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Неделя"):
            expect(
                page.locator(
                    '[data-test-id="createdSelect-1"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Месяц"):
            expect(
                page.locator(
                    '[data-test-id="createdSelect-2"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Тип файла"):
            expect(
                page.locator(
                    '[fieldid="fileType"]'
                    )).to_be_visible()
