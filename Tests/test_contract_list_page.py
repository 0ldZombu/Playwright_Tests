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
contracts_url = getenv('CONTRACTS_LINK')
login_url = getenv("LOGIN_LINK")
base_url = getenv("BASE_URL")


@allure.epic("Список кредитных договоров")
class TestContractPageList:

    @allure.feature("Экранная форма кредитных договоров")
    @allure.title("Проверка экранной формы кредитных договоров")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.contract_list_page
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_contract_list_ui_form(self,
                                   page: Page,
                                   username: str,
                                   password: str
                                   ):
        collection = DirectionMetods(page, url)
        page.set_default_timeout(60000)
        with allure.step("Переход по URL и авторизация UI"):
            collection.go_to(contracts_url)
            expect(page).to_have_url(f"{login_url}")
            collection.login(username, password)
            expect(page).to_have_url(f"{contracts_url}")

        with allure.step("Проверка порядка хлебных крошек"):
            breadcrumbs = page.locator(
                'fnip-breadcrumb fnip-ellipsis-hint span.clamp')
            texts = breadcrumbs.all_inner_texts()
            texts = [t.strip() for t in texts]
            expected = [
                "Единый кабинет",
                "CRM Collection",
                "Кредитные договора"]
            assert texts == expected, f"Ожидалось: {
                expected}, Получено: {texts}"

        with allure.step("Отображение Кредитные договора"):
            expect(
                page.locator(
                    '[data-test-id="filter-header"]'
                    )).to_be_visible()

        with allure.step("Отображение поля с квери поиском"):
            expect(
                page.locator(
                    '[data-test-label="ФИО, паспорт, № КД, VIN"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Дни просрочки"):
            expect(
                page.locator(
                    '[data-test-label="Количество дней просрочки"]'
                    ).nth(0)).to_be_visible()
            page.locator(
                    '[data-test-label="Количество дней просрочки"]'
                    ).nth(0).click()
            expect(
                page.locator(
                    '[data-test-id="from"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="to"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Процесс"):
            expect(
                page.locator(
                    '[data-test-id="workflowStates"]'
                    )).to_be_visible()
            page.locator(
                    '[data-test-id="workflowStates"]'
                    ).click()
            wstates = ["None",
                       "GetEaDocuments",
                       "DelaySendingEmail",
                       "AwaitSendingEmailEvent",
                       "DelayRefinementCft",
                       "RefinementCft",
                       "GenerateFullDebtOrder",
                       "FullOutDebt",
                       "CheckOutDebt",
                       "AwaitFullDebtRemovalConfirmationEvent",
                       "JudicialWork",
                       "End"]
            for _ in wstates:
                expect(
                    page.locator(
                        f'[data-test-id="workflowStates-{_}"]'
                        )).to_be_visible()
            page.locator(
                    '[data-test-id="workflowStates"]'
                    ).click()

        with allure.step("Отображение фильтра Стратегия"):
            expect(
                page.locator(
                    '[data-test-id="strategies"]'
                    )).to_be_visible()
            page.locator(
                    '[data-test-id="strategies"]'
                    ).click()
            strategies = ["Hard_1",
                          "Hard_2",
                          "Soft_1",
                          "Soft_2"]
            for _ in strategies:
                expect(
                    page.locator(
                        f'[data-test-id="strategies-{_}"]'
                        )).to_be_visible()
            page.locator(
                    '[data-test-id="strategies"]'
                    ).click()

        with allure.step("Отображение фильтра Период"):
            expect(
                page.locator(
                    '[data-test-id="creditDate"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение фильтра Сегодня"):
            expect(
                page.locator(
                    '[data-test-id="creditDate-0"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Неделя"):
            expect(
                page.locator(
                    '[data-test-id="creditDate-1"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Месяц"):
            expect(
                page.locator(
                    '[data-test-id="creditDate-2"]'
                    )).to_be_visible()

        with allure.step("Отображение столбца ID"):
            expect(
                page.locator(
                    '[col-id="Id"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Номер кредитного договора"):
            expect(
                page.locator(
                    '[col-id="CreditContractNumber"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Дата кредита"):
            expect(
                page.locator(
                    '[col-id="CreditStartDate"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Тип продукта"):
            expect(
                page.locator(
                    '[col-id="ProductType"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Имя"):
            expect(
                page.locator(
                    '[col-id="person.firstName"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Отчество"):
            expect(
                page.locator(
                    '[col-id="person.patronymic"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Фамилия"):
            expect(
                page.locator(
                    '[col-id="LastName"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Паспорт"):
            expect(
                page.locator(
                    '[col-id="passport"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Сумма кредита"):
            expect(
                page.locator(
                    '[col-id="CreditTotalSum"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца" +
                         " Просроченная задолженность, руб"):
            expect(
                page.locator(
                    '[col-id="OverdueDebt"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Дней просрочки"):
            expect(
                page.locator(
                    '[col-id="DaysDelayFifo"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца КА"):
            expect(
                page.locator(
                    '[col-id="outsourcerName"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Стратегия"):
            expect(
                page.locator(
                    '[col-id="StrategyName"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Состояние"):
            expect(
                page.locator(
                    '[col-id="WorkflowState"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение столбца Теги"):
            expect(
                page.locator(
                    '[col-id="tags"]'
                    ).nth(0)).to_be_visible()

        with allure.step("Отображение кнопок сортировки"):
            eSortIndicator = ["Id",
                              "CreditContractNumber",
                              "CreditStartDate",
                              "ProductType",
                              "LastName",
                              "CreditTotalSum",
                              "OverdueDebt",
                              "DaysDelayFifo",
                              "StrategyName",
                              "WorkflowState"
                              ]
            for _ in eSortIndicator:
                expect(
                    page.locator(f'[col-id={_}]').locator(
                        '[data-ref="eSortIndicator"]')
                ).to_be_visible()

    @allure.feature("Экранная форма кредитных договоров")
    @allure.title("Проверка экранной формы кредитных договоров")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.contract_list_page
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_contract_list_sorting(self,
                                   page: Page,
                                   username: str,
                                   password: str
                                   ):
        collection = DirectionMetods(page, url)
        page.set_default_timeout(60000)
        with allure.step("Переход по URL и авторизация UI"):
            collection.go_to(contracts_url)
            expect(page).to_have_url(f"{login_url}")
            collection.login(username, password)
            expect(page).to_have_url(f"{contracts_url}")

        with allure.step("Проверка порядка хлебных крошек"):
            breadcrumbs = page.locator(
                'fnip-breadcrumb fnip-ellipsis-hint span.clamp')
            texts = breadcrumbs.all_inner_texts()
            texts = [t.strip() for t in texts]
            expected = [
                "Единый кабинет",
                "CRM Collection",
                "Кредитные договора"]
            assert texts == expected, f"Ожидалось: {
                expected}, Получено: {texts}"

        with allure.step("Отображение Кредитные договора"):
            expect(
                page.locator(
                    '[data-test-id="filter-header"]'
                    )).to_be_visible()
