import pytest
import allure
from pathlib import Path
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


@allure.epic("Страница Досье")
class TestContractPage:

    @allure.feature("Вкладка Документы")
    @allure.story("Добавление документа с типом ИНН")
    @allure.title("Добавление двух документов с типом ИНН")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.contract_page
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_add_two_nei(self,
                         page: Page,
                         username: str,
                         password: str
                         ):
        collection = DirectionMetods(page, url)
        page.set_default_timeout(60000)

        with allure.step("Получение токена и загрузка миграции"):
            token = collection.get_token()
            contractNumber, credit_id = collection.post_uploadMigration(
                token,
                person_id=1)

        with allure.step(f"Поиск контракта по номеру: {contractNumber}"):
            query = {"contractNumber": f"{contractNumber}"}
            json_data = collection.get_contracts(token, query_params=query)

        with allure.step("Валидация JSON и получение contract_id"):
            contract_id, person_id = (
                collection.validation_json_to_id_number_contract(
                    json_data,
                    contractNumber))

        with allure.step(
            f"Формирование ссылки для открытия досье: person_id={person_id}," +
             f" contract_id={contract_id}"):
            contract_url = (f"{base_url}/crm-collection/contracts/" +
                            f"client/{person_id}/contract/{contract_id}")

        with allure.step("Переход по URL и авторизация UI"):
            collection.go_to(contract_url)
            expect(page).to_have_url(f"{login_url}")
            collection.login(username, password)
            expect(page).to_have_url(f"{contract_url}")

        with allure.step("Открытие вкладки Документы"):
            page.get_by_role("button", name="Документы").click()

        with allure.step("Проверка что текущий список документов пуст"):
            expect(
                page.get_by_text(
                    "Файл Тип документа Комментарий Оператор Дата загрузки" +
                    " Нет данных для отображения")).to_be_visible()

        for _ in range(2):
            with allure.step("Модалка по добавлению файла с типом ИНН"):
                page.get_by_role("button", name="Добавить").click()
                expect(page.locator(
                    "//div[normalize-space(text())" +
                    "='Тип документа']").get_by_test_id("label-container")
                    ).to_be_visible
                page.get_by_role("textbox", name="Тип документа").click()
                page.get_by_role("textbox", name="Тип документа").fill("ИНН")
                page.locator("[data-test-id=\"type-NEI\"]").click()
                expect(page.locator(
                    "//div[normalize-space(text())" +
                    "='Комментарий']").get_by_test_id("label-container")
                    ).to_be_visible
                page.get_by_role("textbox", name="Комментарий").click()
                page.get_by_role(
                    "textbox", name="Комментарий").fill(
                        "Добавление ИНН автотест")

                with allure.step("Загрузка файла в поле fnip-drag-n-drop"):
                    current_dir = Path(__file__).parent
                    pages_dir = current_dir.parent / "Pages"
                    pdf_path = pages_dir / "input_files" / "PDF.pdf"
                    drag_n_drop = page.locator("fnip-drag-n-drop")
                    file_input = drag_n_drop.locator("input[type='file']")
                    file_input.set_input_files(str(pdf_path))
                    expect(page.get_by_role("img").nth(1)).to_be_visible
                    page.get_by_role("button", name="Сохранить").click()
                    expect(page.get_by_role(
                        "button", name="Сохранить")
                        ).to_be_enabled(timeout=160000)

                with allure.step("Проверка что файл добавлен в документы"):
                    expect(
                        page.get_by_text(
                            "ИНН (Исполнительная Надпись Нотариуса)").first
                        ).to_be_visible

    @allure.feature("Вкладка Документы")
    @allure.story("Добавление документа с типом ИНН")
    @allure.title("Добавление всех валидных типов файлов для ИНН: {file_type}")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.contract_page
    @pytest.mark.parametrize('username, password, file_type', [
        (admin_email, admin_password, "PDF.pdf"),
        (admin_email, admin_password, "JPEG.jpg"),
        (admin_email, admin_password, "RAR.rar"),
        (admin_email, admin_password, "ZIP.zip"),
    ])
    def test_add_nei_all_types(self,
                               page: Page,
                               username: str,
                               password: str,
                               file_type: str):
        collection = DirectionMetods(page, url)
        page.set_default_timeout(60000)

        with allure.step("Получение токена и загрузка миграции"):
            token = collection.get_token()
            contractNumber, credit_id = collection.post_uploadMigration(
                token,
                person_id=1)

        with allure.step(f"Поиск контракта по номеру: {contractNumber}"):
            query = {"contractNumber": f"{contractNumber}"}
            json_data = collection.get_contracts(token, query_params=query)

        with allure.step("Валидация JSON и получение contract_id"):
            contract_id, person_id = (
                collection.validation_json_to_id_number_contract(
                    json_data,
                    contractNumber))

        with allure.step(
            f"Формирование ссылки для открытия досье: person_id={person_id}," +
             " contract_id={contract_id}"):
            contract_url = (f"{base_url}/crm-collection/contracts/" +
                            f"client/{person_id}/contract/{contract_id}")

        with allure.step("Переход по URL и авторизация UI"):
            collection.go_to(contract_url)
            expect(page).to_have_url(f"{login_url}")
            collection.login(username, password)
            expect(page).to_have_url(f"{contract_url}")

        with allure.step("Открытие вкладки Документы"):
            page.get_by_role("button", name="Документы").click()

        with allure.step("Проверка что текущий список документов пуст"):
            expect(
                page.get_by_text(
                    "Файл Тип документа Комментарий Оператор Дата загрузки" +
                    " Нет данных для отображения")).to_be_visible()

        with allure.step(f"Модалка по добавлению {file_type} с типом ИНН"):
            page.get_by_role("button", name="Добавить").click()
            expect(page.locator(
                "//div[normalize-space(text())" +
                "='Тип документа']").get_by_test_id("label-container")
                ).to_be_visible
            page.get_by_role("textbox", name="Тип документа").click()
            page.get_by_role("textbox", name="Тип документа").fill("ИНН")
            page.locator("[data-test-id=\"type-NEI\"]").click()
            expect(page.locator(
                "//div[normalize-space(text())" +
                "='Комментарий']").get_by_test_id("label-container")
                ).to_be_visible
            page.get_by_role("textbox", name="Комментарий").click()
            page.get_by_role(
                "textbox", name="Комментарий").fill(
                    f"Добавление {file_type} автотест")

            with allure.step(
                             f"Загрузка файла {file_type}"):
                current_dir = Path(__file__).parent
                pages_dir = current_dir.parent / "Pages"
                file_path = pages_dir / "input_files" / file_type
                # Прикрепляем информацию о файле к Allure
                allure.attach(
                    (
                        f"Загружаемый файл: {file_type}\n"
                        f"Путь: {file_path}\n"
                        f"Размер: {file_path.stat(

                        ).st_size if file_path.exists(
                        ) else 'Файл не найден'} байт"
                    ),
                    name="Информация о файле",
                    attachment_type=allure.attachment_type.TEXT
                )

                assert file_path.exists(), f"Файл не найден: {file_path}"

                # Загружаем файл
                drag_n_drop = page.locator("fnip-drag-n-drop")
                file_input = drag_n_drop.locator("input[type='file']")
                file_input.set_input_files(str(file_path))
                expect(page.get_by_role("img").nth(1)).to_be_visible
                page.get_by_role("button", name="Сохранить").click()
                expect(page.get_by_role(
                        "button", name="Сохранить")).to_be_enabled(
                            timeout=60000)

            with allure.step(
                             f"Поиск загруженного файла '{file_type}'"):
                expected_file_text = f"Файл {file_type}"
                if file_type == "RAR.rar":
                    expected_file_text = "Файл.rar "
                if file_type == "ZIP.zip":
                    expected_file_text = "Файл.zip"
            with allure.step(f"Поиск текста '{expected_file_text}' в таблице"):
                expect(
                    page.get_by_text(expected_file_text)
                    ).to_be_visible(timeout=5000)

                # Прикрепляем результат к Allure
                allure.attach(
                    f"Файл {file_type} успешно загружен",
                    name=f"Результат загрузки {file_type}",
                    attachment_type=allure.attachment_type.TEXT
                )

    @allure.feature("Вкладка Документы")
    @allure.story("Добавление документа с типом ИНН")
    @allure.title(
        "Добавление всех невалидных типов файлов для ИНН: {file_type}")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.contract_page
    @pytest.mark.parametrize('username, password, file_type', [
        (admin_email, admin_password, "Microsoft Excel.xlsx"),
        (admin_email, admin_password, "Microsoft Word.docx"),
        (admin_email, admin_password, "PNG.png")
    ])
    def test_add_nei_negative_types(self,
                                    page: Page,
                                    username: str,
                                    password: str,
                                    file_type: str):
        collection = DirectionMetods(page, url)
        page.set_default_timeout(60000)

        with allure.step("Получение токена и загрузка миграции"):
            token = collection.get_token()
            contractNumber, credit_id = collection.post_uploadMigration(
                token,
                person_id=1)

        with allure.step(f"Поиск контракта по номеру: {contractNumber}"):
            query = {"contractNumber": f"{contractNumber}"}
            json_data = collection.get_contracts(token, query_params=query)

        with allure.step("Валидация JSON и получение contract_id"):
            contract_id, person_id = (
                collection.validation_json_to_id_number_contract(
                    json_data,
                    contractNumber))

        with allure.step(
            f"Формирование ссылки для открытия досье: person_id={person_id}," +
             " contract_id={contract_id}"):
            contract_url = (f"{base_url}/crm-collection/contracts/" +
                            f"client/{person_id}/contract/{contract_id}")

        with allure.step("Переход по URL и авторизация UI"):
            collection.go_to(contract_url)
            expect(page).to_have_url(f"{login_url}")
            collection.login(username, password)
            expect(page).to_have_url(f"{contract_url}")

        with allure.step("Открытие вкладки Документы"):
            page.get_by_role("button", name="Документы").click()

        with allure.step("Проверка что текущий список документов пуст"):
            expect(
                page.get_by_text(
                    "Файл Тип документа Комментарий Оператор Дата загрузки" +
                    " Нет данных для отображения")).to_be_visible()

        with allure.step(f"Модалка по добавлению {file_type} с типом ИНН"):
            page.get_by_role("button", name="Добавить").click()
            expect(page.locator(
                "//div[normalize-space(text())" +
                "='Тип документа']").get_by_test_id("label-container")
                ).to_be_visible
            page.get_by_role("textbox", name="Тип документа").click()
            page.get_by_role("textbox", name="Тип документа").fill("ИНН")
            page.locator("[data-test-id=\"type-NEI\"]").click()
            expect(page.locator(
                "//div[normalize-space(text())" +
                "='Комментарий']").get_by_test_id("label-container")
                ).to_be_visible
            page.get_by_role("textbox", name="Комментарий").click()
            page.get_by_role(
                "textbox", name="Комментарий").fill(
                    f"Добавление {file_type} автотест")

            with allure.step(
                             f"Загрузка файла {file_type}"):
                current_dir = Path(__file__).parent
                pages_dir = current_dir.parent / "Pages"
                file_path = pages_dir / "input_files" / file_type

                # Прикрепляем информацию о файле к Allure
                allure.attach(
                    (
                        f"Загружаемый файл: {file_type}\n"
                        f"Путь: {file_path}\n"
                        f"Размер: {file_path.stat(

                        ).st_size if file_path.exists(
                        ) else 'Файл не найден'} байт"
                    ),
                    name="Информация о файле",
                    attachment_type=allure.attachment_type.TEXT
                )

                assert file_path.exists(), f"Файл не найден: {file_path}"

                drag_n_drop = page.locator("fnip-drag-n-drop")
                file_input = drag_n_drop.locator("input[type='file']")
                file_input.set_input_files(str(file_path))
                expect(page.get_by_role("img").nth(1)).to_be_visible
                page.get_by_role("button", name="Сохранить").click()
                expect(
                    page.get_by_role("button", name="Сохранить")
                    ).to_be_enabled(timeout=160000)
            with allure.step(
                             f"Негативный аллер для'{file_type}'"):
                expect(page.get_by_role("alert"),
                       "Алерт не появился").to_be_visible()

    @allure.feature("Вкладка Документы")
    @allure.story("Добавление документа с типом ИНОЕ")
    @allure.title("Добавление двух документов с типом ИНОЕ")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.contract_page
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_add_two_other(self,
                           page: Page,
                           username: str,
                           password: str
                           ):
        collection = DirectionMetods(page, url)
        page.set_default_timeout(60000)

        with allure.step("Получение токена и загрузка миграции"):
            token = collection.get_token()
            contractNumber, credit_id = collection.post_uploadMigration(
                token,
                person_id=1)

        with allure.step(f"Поиск контракта по номеру: {contractNumber}"):
            query = {"contractNumber": f"{contractNumber}"}
            json_data = collection.get_contracts(token, query_params=query)

        with allure.step("Валидация JSON и получение contract_id"):
            contract_id, person_id = (
                collection.validation_json_to_id_number_contract(
                    json_data,
                    contractNumber))

        with allure.step(
            f"Формирование ссылки для открытия досье: person_id={person_id}," +
             " contract_id={contract_id}"):
            contract_url = (f"{base_url}/crm-collection/contracts/" +
                            f"client/{person_id}/contract/{contract_id}")

        with allure.step("Переход по URL и авторизация UI"):
            collection.go_to(contract_url)
            expect(page).to_have_url(f"{login_url}")
            collection.login(username, password)
            expect(page).to_have_url(f"{contract_url}")

        with allure.step("Открытие вкладки Документы"):
            page.get_by_role("button", name="Документы").click()

        with allure.step("Проверка что текущий список документов пуст"):
            expect(
                page.get_by_text(
                    "Файл Тип документа Комментарий Оператор Дата загрузки" +
                    " Нет данных для отображения")).to_be_visible()

        for _ in range(2):
            with allure.step("Модалка по добавлению файла с типом ИНОЕ"):
                page.get_by_role("button", name="Добавить").click()
                expect(page.locator(
                    "//div[normalize-space(text())" +
                    "='Тип документа']").get_by_test_id("label-container")
                    ).to_be_visible
                page.get_by_role("textbox", name="Тип документа").click()
                page.get_by_role("textbox", name="Тип документа").fill("ИНОЕ")
                page.locator("[data-test-id=\"type-Other\"]").click()
                expect(page.locator(
                    "//div[normalize-space(text())" +
                    "='Комментарий']").get_by_test_id("label-container")
                    ).to_be_visible
                page.get_by_role("textbox", name="Комментарий").click()
                page.get_by_role(
                    "textbox", name="Комментарий").fill(
                        "Добавление ИНОЕ автотест")

                with allure.step("Загрузка файла в поле fnip-drag-n-drop"):
                    current_dir = Path(__file__).parent
                    pages_dir = current_dir.parent / "Pages"
                    pdf_path = pages_dir / "input_files" / "PDF.pdf"
                    drag_n_drop = page.locator("fnip-drag-n-drop")
                    file_input = drag_n_drop.locator("input[type='file']")
                    file_input.set_input_files(str(pdf_path))
                    expect(page.get_by_role("img").nth(1)).to_be_visible
                    page.get_by_role("button", name="Сохранить").click()

                with allure.step("Проверка что файл добавлен в документы"):
                    expect(
                        page.get_by_text(
                            "ИНОЕ").first
                        ).to_be_visible

    @allure.feature("Вкладка График Платежей")
    @allure.story("Валидация порядка колонок")
    @allure.title("Валидация переноса колонки Тип операций")
    @pytest.mark.regression
    @pytest.mark.contract_page
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_validation_column_payments(self,
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

        with allure.step("Открытие вкладки График платежей"):
            expect(
                page.locator(
                    "//a[@data-appearance='action-button']"
                    ).nth(0)).to_be_visible
            page.locator(
                    "//a[@data-appearance='action-button']"
                    ).nth(0).click()
            expect(
                page.get_by_role(
                    "button", name="График платежей")
                    ).to_be_visible
            page.get_by_role("button", name="График платежей").click()

        with allure.step("Проверка последовательности вкладок"):
            assert page.locator(
                '(//span[@data-ref="eText"])[2]'
                ).inner_text() == "Дата платежа"
            assert page.locator(
                '(//span[@data-ref="eText"])[3]'
                ).inner_text() == "Тип операции"

    @allure.feature("Основная информация по Досье")
    @allure.story("Интерфейс карточки досье")
    @allure.title("Валидация переноса таба Участники")
    @pytest.mark.regression
    @pytest.mark.contract_page
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_validation_contract_tabs(self,
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

        with allure.step("Открытие основной страницы Досье"):
            expect(
                page.locator(
                    "//a[@data-appearance='action-button']"
                    ).nth(0)).to_be_visible
            page.locator(
                    "//a[@data-appearance='action-button']"
                    ).nth(0).click()
        with allure.step("Валидация переноса Участники в конец"):
            assert page.locator(
                "xpath=(//span[@class='t-highlight'])[last()-1]"
                ).inner_text() == "Участники"

    @allure.feature("Основная информация по Досье")
    @allure.story("Интерфейс карточки досье")
    @allure.title("Валидация отображения данных в 1 строку")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.contract_page
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_validation_one_line_data_contract(self,
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

        with allure.step("Открытие основной страницы Досье"):
            expect(
                page.locator(
                    "//a[@data-appearance='action-button']"
                    ).nth(0)).to_be_visible
            page.locator(
                    "//a[@data-appearance='action-button']"
                    ).nth(0).click()
        with allure.step("Валидация отображения данных в 1 строку"):
            assert expect(page.locator("//div[@role='group']")).to_be_visible

    @allure.feature("Основная информация по Досье")
    @allure.story("Вкладка Залог")
    @allure.title("Отображение данные в Наличие обеспечения")
    @pytest.mark.regression
    @pytest.mark.contract_page
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_validation_have_security(self,
                                      page: Page,
                                      username: str,
                                      password: str
                                      ):

        collection = DirectionMetods(page, url)
        page.set_default_timeout(60000)

        with allure.step("Получение токена и загрузка миграции"):
            token = collection.get_token()
            contractNumber, credit_id = collection.post_uploadMigration(
                token,
                person_id=1,
                have_security=True)

        with allure.step(f"Поиск контракта по номеру: {contractNumber}"):
            query = {"contractNumber": f"{contractNumber}"}
            json_data = collection.get_contracts(token, query_params=query)

        with allure.step("Валидация JSON и получение contract_id"):
            contract_id, person_id = (
                collection.validation_json_to_id_number_contract(
                    json_data,
                    contractNumber))

        with allure.step("Формирование ссылки для открытия досье:" +
                         f" person_id={person_id}, contract_id={contract_id}"):
            contract_url = (f"{base_url}/crm-collection/contracts/" +
                            f"client/{person_id}/contract/{contract_id}")

        with allure.step("Переход по URL и авторизация UI"):
            collection.go_to(contract_url)
            expect(page).to_have_url(f"{login_url}")
            collection.login(username, password)
            expect(page).to_have_url(f"{contract_url}")

        with allure.step("Открытие вкладки Залог"):
            page.get_by_role("button", name="Залог").click()

        with allure.step("Получение данных Наличие обеспечения"):
            have_security = page.locator(
                    'fnip-labeled-content:has' +
                    '(label:has-text("Наличие обеспечения"))')
            expect(have_security).to_be_visible
            value_security = have_security.locator(
                '.content p, .content span').first.inner_text()
            assert value_security == "Да"

        with allure.step("Повторная миграция"):
            contractNumber, credit_id = collection.post_uploadMigration(
                token,
                person_id=1,
                override_contract=True,
                have_security=False,
                credit_id=credit_id)

        with allure.step("Обнолвение страницы"):
            page.reload()

        with allure.step("Открытие вкладки Залог"):
            expect(page.get_by_role("button", name="Залог")).to_be_visible
            page.get_by_role("button", name="Залог").click()

        with allure.step("Повторное получение данных Наличие обеспечения"):
            have_security = page.locator(
                    'fnip-labeled-content:has' +
                    '(label:has-text("Наличие обеспечения"))')
            expect(have_security).to_be_visible
            value_security = have_security.locator(
                '.content p, .content span').first.inner_text()
            assert value_security == "Нет"
