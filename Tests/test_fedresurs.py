import urllib3
import pytest
import allure
from os import getenv
from dotenv import load_dotenv
from playwright.sync_api import expect, Page
from Pages.direction_metods import DirectionMetods
from Pages.fedresurs_generate import (generate_excel_file_with_date,
                                      validate_error_column,
                                      validate_fedresurs_xml,
                                      get_expected_values_from_excel)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv(override=True)

admin_email = getenv('ADMIN_EMAIL')
admin_password = getenv('ADMIN_PASSWORD')
url = getenv('URL')
login_url = getenv("LOGIN_LINK")
fedresurs_url = getenv("FEDRESURS_LINK")
type1 = 'InclusionDebtorsToDebtCollectorList2'
typeLocator1 = (
    'Привлечение кредитором представителя кредитора' +
    ' для взаимодействия с должником')
type2 = 'DebtCollectors.Participants.Company'
typeLocator2 = 'Переход права требования к иному лицу (цессия)'
type3 = 'DebtCollectors.Participants.Person'
type4 = 'DebtCollectors.Participants.NonResidentCompany'
type5 = 'DebtCollectors.Participants.IndividualEntrepreneur'


@allure.epic("Федресурс")
class TestFedresurs:

    @allure.feature("Генерация Федресурс")
    @allure.story("Проверка генерации XML для разных типов уведомлений")
    @allure.title("Генерация и валидация XML-файла Федресурс для типа: {type}")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.fedresurs
    @pytest.mark.parametrize('username, password, type', [
        (admin_email, admin_password, f"{type1}"),
        (admin_email, admin_password, f"{type2}"),
        (admin_email, admin_password, f"{type3}"),
        (admin_email, admin_password, f"{type4}"),
        (admin_email, admin_password, f"{type5}")
    ])
    def test_fedresurs(self,
                       page: Page,
                       username: str,
                       password: str,
                       type: str,
                       ):
        with allure.step("Авторизация"):
            collection = DirectionMetods(page, url)
            collection.go_to(fedresurs_url)
            collection.login(username, password)
            expect(page).to_have_url(f"{fedresurs_url}")

        with allure.step("Переход в раздел Федресурс"):
            page.get_by_role("heading", name="Федресурс").click()
            expect(
                page.locator(
                    "#manual-notification-generation").get_by_role(
                        "button", name="Ручная генерация уведомления")
                        ).to_be_visible()
            expect(
                page.locator(
                    "fnip-button").filter(
                        has_text="Сформировать XML")).to_be_visible()

        with allure.step("Выбор коллекторского агентства"):
            page.get_by_role(
                "textbox", name="Коллекторское агентство *").click()
            page.locator('[role="listbox"] button[role="option"]'
                         ).nth(0).click()

        with allure.step(f"Выбор типа уведомления: {type}"):
            page.get_by_role("textbox", name="Тип уведомлений *").click()
            if type is type1:
                typelocator = typeLocator1
            else:
                typelocator = typeLocator2
            page.get_by_role("option", name=f"{typelocator}").click()

        with allure.step("Выбор кредитора"):
            page.get_by_role("textbox", name="Кредитор *").click()
            page.locator('[role="listbox"] button[role="option"]'
                         ).nth(0).click()

        with allure.step("Генерация и загрузка Excel-файла"):
            file = generate_excel_file_with_date(type)
            page.locator(
                "fnip-reactive-file-input input[type='file']"
                ).set_input_files(file)

        with allure.step("Формирование XML"):
            page.get_by_role("button", name="Сформировать XML").click()
            page.locator(
                "fnip-button").filter(has_text="Сформировать XML").click()

        with allure.step("Скачивание XML-файла"):
            try:
                with page.expect_download(timeout=20000) as download_info:
                    page.get_by_role("button", name="fedresurs"
                                     ).click()
                download = download_info.value
            except Exception as e:
                allure.attach(
                    f"Ошибка при скачивании XML-файла: {str(e)}\n",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise AssertionError(
                    f"Не удалось скачать XML-файл: {str(e)}") from e

        with allure.step("Проверка скачанного файла"):
            assert download.suggested_filename.endswith(
                '.xml'), "Неверный формат файла"
            assert download.path() is not None, "Файл не скачался"

        with allure.step("Получение ожидаемых значений из Excel"):
            expected_values = get_expected_values_from_excel(file, type)

        with allure.step("Валидация XML-файла"):
            # Проверяем XML
            validate_fedresurs_xml(download.path(), expected_values, type)

    @allure.feature("Форма Федресурс")
    @allure.story("Проверка обязательных полей")
    @allure.title("Алерт об обязательности обязательных полей")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.fedresurs
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_fedresurs_validation(self,
                                  page: Page,
                                  username: str,
                                  password: str):
        with allure.step("Авторизация"):
            collection = DirectionMetods(page, url)
            collection.go_to(fedresurs_url)
            collection.login(username, password)
            expect(page).to_have_url(f"{fedresurs_url}")

        with allure.step("Переход в раздел Федресурс"):
            page.get_by_role("heading", name="Федресурс").click()
            expect(
                page.locator(
                    "#manual-notification-generation").get_by_role(
                        "button", name="Ручная генерация уведомления")
                        ).to_be_visible()

        with allure.step("Наличие поля 'Файл с данными для генерации'"):
            expect(
                page.get_by_text("Файл с данными для генерации")
                ).to_be_visible()
            page.get_by_text("Файл с данными для генерации").click()

        with allure.step("Наличие поля 'Аутсорсер'"):
            expect(
                page.locator("[data-test-id=\"outsourcerId\"]"
                             ).get_by_test_id(
                                 "label-container")).to_be_visible()
            page.locator(
                "[data-test-id=\"outsourcerId\"]"
                ).get_by_test_id("label-container").click()

        with allure.step("Наличие поля 'Тип файла'"):
            expect(
                page.locator(
                    "[data-test-id=\"fileType\"]"
                    ).get_by_test_id("label-container")).to_be_visible()
            page.locator(
                "[data-test-id=\"fileType\"]"
                ).get_by_test_id(
                    "label-container").click()

        with allure.step("Наличие поля 'Тип публикатора'"):
            expect(
                page.locator(
                    "[data-test-id=\"publisherType\"]"
                    ).get_by_test_id("label-container")).to_be_visible()
            page.locator(
                "[data-test-id=\"publisherType\"]"
                ).get_by_test_id("label-container").click()

        with allure.step("Наличие поля 'Кредитор'"):
            expect(
                page.locator(
                    "[data-test-id=\"creditorId\"]"
                    ).get_by_test_id("label-container")).to_be_visible()
            page.locator(
                "[data-test-id=\"creditorId\"]"
                ).get_by_test_id("label-container").click()

        with allure.step("Наличие поля 'Полное наименование публикатора'"):
            expect(
                page.locator(
                    "[data-test-id=\"publisherFullName\"]"
                    ).get_by_test_id("label-container")).to_be_visible()
            page.locator(
                "[data-test-id=\"publisherFullName\"]"
                ).get_by_test_id("label-container").click()

        with allure.step("Наличие поля 'ИНН публикатора'"):
            expect(
                page.locator(
                    "[data-test-id=\"publisherInn\"]"
                    ).get_by_test_id("label-container")).to_be_visible()
            page.locator(
                "[data-test-id=\"publisherInn\"]"
                ).get_by_test_id("label-container").click()

        with allure.step("Наличие поля 'ОГРН организации'"):
            expect(page.get_by_text("ОГРН организации")).to_be_visible()
            page.get_by_text("ОГРН организации").click()

        with allure.step("Попытка отправки формы без заполнения"):
            expect(
                page.locator(
                    "fnip-button").filter(
                        has_text="Сформировать XML")).to_be_visible()
            page.locator(
                "fnip-button").filter(has_text="Сформировать XML").click()
            page.get_by_text(
                "Присутствуют ошибки в форме," +
                " проверьте поля: • Файл с данными для генерации • Ти").click()

        with allure.step("Проверка сообщений" +
                         " об ошибках для обязательных полей"):
            page.locator(
                "[data-test-id=\"outsourcerId\"]"
                ).get_by_text("Поле обязательно для заполнения").click()
            page.locator(
                "[data-test-id=\"fileType\"]"
                ).get_by_text("Поле обязательно для заполнения").click()
            page.locator(
                "[data-test-id=\"creditorId\"]"
                ).get_by_text("Поле обязательно для заполнения").click()

    @allure.feature("Генерация Федресурс")
    @allure.story("Проверка генерации XML для разных типов уведомлений")
    @allure.title("Негативная генерация и валидация " +
                  "XML-файла Федресурс для типа: {type}")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.fedresurs
    @pytest.mark.parametrize('username, password, type', [
        (admin_email, admin_password, f"{type1}"),
        (admin_email, admin_password, f"{type2}"),
        (admin_email, admin_password, f"{type3}"),
        (admin_email, admin_password, f"{type4}"),
        (admin_email, admin_password, f"{type5}")
    ])
    def test_fedresurs_negative(self,
                                page: Page,
                                username: str,
                                password: str,
                                type: str,
                                ):
        with allure.step("Авторизация"):
            collection = DirectionMetods(page, url)
            # Запросы для генерации и загрузки досье в систему
            collection.go_to(fedresurs_url)
            collection.login(username, password)
            expect(page).to_have_url(f"{fedresurs_url}")

        with allure.step("Переход в раздел Федресурс"):
            page.get_by_role("heading", name="Федресурс").click()
            expect(
                page.locator(
                    "#manual-notification-generation").get_by_role(
                        "button", name="Ручная генерация уведомления")
                        ).to_be_visible()
            expect(
                page.locator(
                    "fnip-button").filter(
                        has_text="Сформировать XML")).to_be_visible()

        with allure.step("Выбор коллекторского агентства"):
            page.get_by_role(
                "textbox", name="Коллекторское агентство *").click()
            page.locator('[role="listbox"] button[role="option"]'
                         ).nth(0).click()

        with allure.step(f"Выбор типа уведомления: {type}"):
            page.get_by_role("textbox", name="Тип уведомлений *").click()
            if type is type1:
                typelocator = typeLocator2
            else:
                typelocator = typeLocator1
            page.get_by_role("option", name=f"{typelocator}").click()

        with allure.step("Выбор кредитора"):
            page.get_by_role("textbox", name="Кредитор *").click()
            page.locator('[role="listbox"] button[role="option"]'
                         ).nth(0).click()

        with allure.step("Генерация и загрузка Excel-файла"):
            file = generate_excel_file_with_date(type)
            page.locator(
                "fnip-reactive-file-input input[type='file']"
                ).set_input_files(file)

        with allure.step("Формирование XML"):
            page.get_by_role("button", name="Сформировать XML").click()
            page.locator(
                "fnip-button").filter(has_text="Сформировать XML").click()

        with allure.step("Сформировн файл с ошибками генерации"):
            expect(
                page.locator(
                    'h2:has-text("Скачать файлы с ошибками")'
                    )).to_be_visible()

        with allure.step("Скачивание файла"):
            try:
                with page.expect_download(timeout=20000) as download_info:
                    page.get_by_role("link", name="Ошибки генерации").click()
                download = download_info.value
            except Exception as e:
                allure.attach(
                    f"Ошибка при скачивании файла: {str(e)}\n",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise AssertionError(
                    f"Не удалось скачать файл: {str(e)}") from e

        with allure.step("Проверка скачанного файла"):
            assert download.suggested_filename.endswith(
                '.xlsx'), "Неверный формат файла"
            assert download.path() is not None, "Файл не скачался"

        with allure.step("Валидация Excel-файла с ошибками"):
            validate_error_column(download.path())

    @allure.feature("Экранная форма Федресурс")
    @allure.title("Проверка экранной формы федресурс")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.fedresurs
    @pytest.mark.parametrize('username, password, type', [
        (admin_email, admin_password, f"{type1}")
    ])
    def test_fedresurs_ui_form(self,
                               page: Page,
                               username: str,
                               password: str,
                               type: str,):
        with allure.step("Авторизация"):
            collection = DirectionMetods(page, url)
            collection.go_to(fedresurs_url)
            collection.login(username, password)
            expect(page).to_have_url(f"{fedresurs_url}")

        with allure.step("Переход в раздел Федресурс"):
            page.get_by_role("heading", name="Федресурс").click()
            expect(
                page.locator(
                    "#manual-notification-generation").get_by_role(
                        "button", name="Ручная генерация уведомления")
                        ).to_be_visible()
            expect(
                page.locator(
                    "fnip-button").filter(
                        has_text="Сформировать XML")).to_be_visible()

        with allure.step("Отображение коллекторского агентства"):
            expect(page.get_by_role(
                "textbox", name="Коллекторское агентство *")).to_be_visible()
            page.get_by_role(
                "textbox", name="Коллекторское агентство *").click()
            expect(page.locator('[role="listbox"] button[role="option"]'
                                ).nth(0)).to_be_visible()

        with allure.step("Отображение типа уведомления"):
            expect(
                page.get_by_role(
                    "textbox", name="Тип уведомлений *"
                    )).to_be_visible()
            page.get_by_role("textbox", name="Тип уведомлений *").click()
            expect(
                page.get_by_role(
                    "option", name=f"{typeLocator1}")).to_be_visible()
            expect(
                page.get_by_role(
                    "option", name=f"{typeLocator2}")).to_be_visible()

        with allure.step("Отображение кредитора"):
            expect(
                page.get_by_role(
                    "textbox", name="Кредитор *")).to_be_visible()
            page.get_by_role("textbox", name="Кредитор *").click()
            expect(
                page.locator('[role="listbox"] button[role="option"]'
                             ).nth(0)).to_be_visible()

        with allure.step("Отображение публикатора"):
            expect(
                page.get_by_label("Тип публикатора")).to_be_visible()

        with allure.step("Отображение Наименование орг"):
            expect(
                page.get_by_label(
                    "Полное наименование организации")
                    ).to_be_visible()

        with allure.step("Отображение ИНН организации"):
            expect(
                page.get_by_label(
                    "ИНН организации")
                    ).to_be_visible()

        with allure.step("Отображение ОГРН организации"):
            expect(
                page.get_by_label(
                    "ОГРН организации")
                    ).to_be_visible()

        with allure.step("Отображение Формирование XML"):
            expect(
                page.get_by_role(
                    "button", name="Сформировать XML")).to_be_visible()

        with allure.step("Отображение Список сгенерированных"):
            expect(
                page.locator(
                    "#generated-notifications-list").get_by_role(
                        "button", name="Список сгенерированных уведомлений")
                        ).to_be_visible()

        with allure.step("Отображение фильтра Кредитор Коллектор"):
            expect(page.get_by_role(
                "textbox", name="Кредитор, коллектор")).to_be_visible()

        with allure.step("Отображение фильтра Дата"):
            expect(page.get_by_role(
                "textbox", name="Дата")).to_be_visible()

        with allure.step("Отображение фильтра Тип"):
            expect(
                page.locator(
                    '[data-test-id="filterMessageType"]'
                    )).to_be_visible()
            page.locator(
                    '[data-test-id="filterMessageType"]'
                    ).click()
            expect(
                page.locator(
                    '[data-test-id="filterMessageType' +
                    '-InclusionDebtorsToDebtCollectorList2"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="filterMessageType-AssignmentOfClaim"]'
                    )).to_be_visible()

        with allure.step("Отображение фильтра Статус"):
            expect(
                page.locator(
                    '[data-test-id="filterStatus"]'
                    )).to_be_visible()
            page.locator(
                    '[data-test-id="filterStatus"]'
                    ).click()
            expect(
                page.locator(
                    '[data-test-id="filterStatus-Error"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="filterStatus-Exported"]'
                    )).to_be_visible()
            expect(
                page.locator(
                    '[data-test-id="filterStatus-Created"]'
                    )).to_be_visible()
            page.locator(
                    '[data-test-id="filterStatus"]'
                    ).click()

        with allure.step("Отображение столбца ID"):
            expect(
              page.locator('.ag-header-cell-text:has-text("ID")')
              ).to_be_visible()

        with allure.step("Отображение столбца Тип уведомления"):
            expect(
              page.locator('.ag-header-cell-text:has-text("Тип уведомления")')
              ).to_be_visible()

        with allure.step("Отображение столбца Дата генерации"):
            expect(
              page.locator('.ag-header-cell-text:has-text("Дата генерации")')
              ).to_be_visible()

        with allure.step("Отображение столбца Кредитор"):
            expect(
              page.locator('.ag-header-cell-text:has-text("Кредитор")')
              ).to_be_visible()

        with allure.step("Отображение столбца Коллектор"):
            expect(
              page.locator('.ag-header-cell-text:has-text("Коллектор")')
              ).to_be_visible()

        with allure.step("Отображение кнопки скачивания"):
            expect(
                page.locator(
                    'button[data-appearance="action-button"]'
                    ).first).to_be_visible()
