import urllib3
import pytest
import re
import allure
import os
import shutil
from docx2pdf import convert
from os import getenv
from dotenv import load_dotenv
from playwright.sync_api import expect, Page
from Pages.direction_metods import DirectionMetods
from Pages.generate_pdf import generate_pdf

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv(override=True)

admin_email = getenv('ADMIN_EMAIL')
admin_password = getenv('ADMIN_PASSWORD')
url = getenv('URL')
login_url = getenv("LOGIN_LINK")
base_url = getenv("BASE_URL")


@allure.epic("CRM direction")
@allure.feature("Работа с договорами")
class TestProcessContract:

    @allure.title("Бизнес процесс по досье")
    @allure.description(
        "Тест проверяет полный цикл обработки договора:" +
        " создание, скачивание письма, подтверждение отправки, вынос")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.skip(
        reason="Из-за ограничения ЦФТ необходимо указывать номер досье руками")
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_process_contract(self,
                              page: Page,
                              username: str,
                              password: str):
        direction = DirectionMetods(page, url)
        page.set_default_timeout(60000)

        with allure.step("Получение токена и загрузка миграции"):
            token = direction.get_token()
            contractNumber, credit_id = direction.post_uploadMigration(
                token,
                person_id=2)

        with allure.step(f"Поиск контракта по номеру: {contractNumber}"):
            query = {"contractNumber": f"{contractNumber}"}
            json_data = direction.get_contracts(token, query_params=query)

        with allure.step("Валидация JSON и получение contract_id"):
            contract_id, person_id = (
                direction.validation_json_to_id_number_contract(
                    json_data,
                    contractNumber))

        with allure.step("Запуск workflow контракта"):
            direction.start_workflow_contract(
                token,
                contractId=contract_id,
                loanDate=direction.get_time("%Y-%m-%d"),
                overdueDate=direction.get_time("%Y-%m-%d"))

        with allure.step("Формирование ссылки для открытия досье:" +
                         f" person_id={person_id}, contract_id={contract_id}"):
            contract_url = (f"{base_url}/crm-direction/contracts/" +
                            f"client/{person_id}/contract/{contract_id}")

        with allure.step("Переход по URL и авторизация UI"):
            direction.go_to(contract_url)
            expect(page).to_have_url(f"{login_url}")
            direction.login(username, password)
            expect(page).to_have_url(f"{contract_url}")

        with allure.step("Проверка видимости кнопки" +
                         " 'Подтвердить отправку письма'"):
            expect(page.get_by_role(
                "button", name="Подтвердить отправку письма")).to_be_visible(
                    timeout=60000)

        download = None
        docx_path = None

        with allure.step("Скачивание письма-требования и конвертация в PDF"):
            with page.expect_download() as download_info:
                page.get_by_role(
                    "button", name="Скачать письмо-требование").click()
                expect(page.locator("button").filter(
                    has_text="Скачать")).not_to_have_class(
                        "_disabled", timeout=120000)
                expect(page.locator("button").filter(
                    has_text="Скачать")).not_to_have_class(
                        "_loading", timeout=120000)
                expect(page.locator("button").filter(
                    has_text="Скачать")).to_be_enabled(timeout=120000)

                download = download_info.value

                # Создаём папку files в директории теста, если её нет
                current_dir = os.path.dirname(os.path.abspath(__file__))
                files_dir = os.path.join(current_dir, "files")
                os.makedirs(files_dir, exist_ok=True)

                # Сохраняем DOCX файл с именем "Письмо-требование.docx"
                docx_path = os.path.join(files_dir, "Письмо-требование.docx")
                shutil.copy(str(download.path()), docx_path)

                # Конвертируем в PDF с именем "Письмо-требование.pdf"
                pdf_path = os.path.join(files_dir, "Письмо-требование.pdf")
                convert(docx_path, pdf_path)

        # Прикрепляем PDF к Allure
        allure.attach.file(
            pdf_path,
            name="Письмо-требование (PDF)",
            attachment_type=allure.attachment_type.PDF)

        with allure.step("Проверка скачанного файла"):
            assert download is not None
            expect(page.get_by_text("Ошибка при скачивании"),
                   "Алерт с ошибкой ЦФТ не появился").to_be_hidden()

        with allure.step("Подтверждение отправки письма"):
            page.get_by_role(
                "button", name="Подтвердить отправку письма").click()

        with allure.step("Заполнение ШПИ и даты отправки"):
            page.get_by_role("textbox", name="ШПИ *").click()
            page.get_by_role("textbox", name="ШПИ *").fill("123321123321")
            page.locator(
                "[data-test-id=\"postalSentDate\"]").get_by_role("img").click()
            page.get_by_role("button", name="Предыдущий").click()
            page.get_by_role("button", name="Предыдущий").click()
            page.get_by_text("1", exact=True).first.click()

            files_block = page.locator("fnip-files-block")
            file_input = files_block.locator("input[type='file']")
            file_input.set_input_files(pdf_path)

            expect(
                files_block.get_by_text(
                    "Письмо-требование.pdf")
                    ).to_be_visible()

            page.get_by_role("button", name="Сохранить").click()

        with allure.step("Ожидание подтверждения ПВ"):
            expect(
                page.get_by_text(
                    "Ожидание подтверждения ПВ")).to_be_visible(timeout=180000)
            page.get_by_text("Ожидание подтверждения ПВ").click()

        with allure.step("Подтверждение полного выноса"):
            page.get_by_role("button", name="Подтвердить полный вынос").click()
            page.get_by_role(
                "heading", name="Подтверждение полного выноса").click()
            page.locator("fnip-files-block").get_by_text(
                "Расчет задолженности на дату").click()
            page.locator('[data-test-id="fileFc"] input[type="file"]'
                         ).set_input_files(
                    generate_pdf(1))

        with allure.step("Проверка перехода в 'Судебное производство'"):
            expect(
                page.get_by_text("Судебное производство")).to_be_visible(
                    timeout=180000)
            page.get_by_role("img").nth(3).click()
            page.locator(
                    '[data-test-label="Сохранить"]'
                    ).click()
            page.locator(".flex-shrink-0 > button").first.click()
            expect(
                page.get_by_text("Судебное производство")).to_be_visible(
                    timeout=180000)
            expect(page.get_by_text("Полный вынос")).to_be_visible()

    @allure.title("Бизнес процесс по досье - ошибка ЦФТ")
    @allure.description(
        "Тест проверяет отображение ошибки" +
        " ЦФТ при скачивании письма-требования")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_process_contract_error_cft(self,
                                        page: Page,
                                        username: str,
                                        password: str):
        direction = DirectionMetods(page, url)

        with allure.step("Формирование ссылки для открытия досье:" +
                         " person_id=8229, contract_id=7661"):
            person_id = 8229
            contract_id = 7661
            contract_url = (f"{base_url}/crm-direction/contracts/" +
                            f"client/{person_id}/contract/{contract_id}")

        with allure.step("Переход по URL и авторизация UI"):
            direction.go_to(contract_url)
            expect(page).to_have_url(f"{login_url}")
            direction.login(username, password)
            expect(page).to_have_url(f"{contract_url}")

        with allure.step("Проверка видимости кнопки" +
                         " 'Подтвердить отправку письма'"):
            expect(page.get_by_role(
                "button", name="Подтвердить отправку письма"),
                "Кнопка Подтвердить отправку письма не найдена"
                ).to_be_visible()

        with allure.step("Попытка скачивания письма-требования"):
            page.get_by_role(
                "button", name="Скачать письмо-требование"
                ).click()
            expect(page.locator("button").filter(
                has_text="Скачать")).not_to_have_class(
                    "_disabled", timeout=120000)
            expect(page.locator("button").filter(
                has_text="Скачать")).not_to_have_class(
                    "_loading", timeout=120000)
            expect(page.locator("button").filter(
                has_text="Скачать")).to_be_enabled(timeout=120000)

        with allure.step("Проверка отображения ошибки ЦФТ"):
            expect(page.get_by_text("Ошибка при скачивании"),
                   "Алерт с ошибкой ЦФТ не появился").to_be_visible()
            page.get_by_text("Ошибка при скачивании").click()

    @allure.title("Бизнес процесс по ИНН ")
    @allure.description(
        "Тест проверяет полный цикл работы с ИНН:" +
        " подача документов нотариусу, оплата пошлины," +
        " указание реквизитов ИНН")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.nei
    @pytest.mark.skip(
        reason="Из-за ограничения ЦФТ необходимо указывать номер досье руками")
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    def test_process_nei(self,
                         page: Page,
                         username: str,
                         password: str):
        direction = DirectionMetods(page, url)
        page.set_default_timeout(60000)

        with allure.step("Получение токена и загрузка миграции"):
            # Запросы для генерации и загрузки досье в систему
            token = direction.get_token()
            contractNumber, credit_id = direction.post_uploadMigration(
                token,
                person_id=3)

        with allure.step(f"Поиск контракта по номеру: {contractNumber}"):
            query = {"contractNumber": f"{contractNumber}"}
            json_data = direction.get_contracts(token, query_params=query)

        with allure.step("Валидация JSON и получение contract_id"):
            # Валидируем JSON и получаем contract_id для запуска процесса
            contract_id, person_id = (
                direction.validation_json_to_id_number_contract(
                    json_data,
                    contractNumber))

        with allure.step("Создание JudicialWork" +
                         " и запуск workflow НЕИ"):
            nei_id = direction.post_JudicialWork(
                token,
                contractId=contract_id)
            direction.start_workflow_nei(token,
                                         contractId=contract_id,
                                         neiId=nei_id)

        with allure.step("Формирование ссылки для открытия досье:" +
                         f" person_id={person_id}, contract_id={contract_id}"):
            # Формируем ссылку для открытия досье с contract_id, person_id
            contract_url = (f"{base_url}/crm-direction/contracts/" +
                            f"client/{person_id}/contract/{contract_id}")

        with allure.step("Переход по URL и авторизация UI"):
            direction.go_to(contract_url)
            expect(direction.page).to_have_url(f"{login_url}")
            direction.login(username, password)
            expect(page.locator(
                "fnip-toolbar").get_by_text("CRM direction")).to_be_visible()

        with allure.step(f"Поиск контракта {contractNumber} в списке"):
            page.get_by_role("link").nth(4).click()
            page.get_by_role(
                "textbox", name="Номер кредитного договора"
                ).click()
            page.get_by_role(
                "textbox", name="Номер кредитного договора").fill(
                    f"{contractNumber}")
            expect(page.locator(".t-tag > .t-icon > .t-svg")).to_be_visible()
            page.locator(".t-tag > .t-icon > .t-svg").click()
            page.get_by_role("link").filter(
                has_text=re.compile(r"^$")).nth(4).click()

        with allure.step("Подача документов нотариусу"):
            page.get_by_text("Подача документов нотариусу").first.click()
            page.get_by_role("button",
                             name="Указать данные по подаче документов"
                             ).click()
            page.get_by_role("textbox", name="Сумма задолженности *").click()
            page.get_by_role("textbox", name="Сумма задолженности *").fill(
                    "123123123")
            page.locator(".t-box > .t-content").click()
            page.get_by_role(
                "textbox", name="Информация о платеже из ЛК нотариата").click()
            page.get_by_role(
                "textbox",
                name="Информация о платеже из ЛК нотариата").fill(
                    "Номер заявления\n021-260306-50326-32\n\n" +
                    "ФИО нотариуса\nЯковлева Василиса Васильевна\n\n" +
                    "Адрес нотариуса\n453130, Респ Башкортостан," +
                    " г Стерлитамак, ул Суханова, д 212б\n\n" +
                    "ИНН нотариуса\n027711925947\n\nНазначение платежа\n" +
                    "Оплата нотариального действия - Совершение удалённо" +
                    " исполнительной надписи о взыскании денежных сумм" +
                    " или истребовании имущества от должника по заявлению" +
                    " №03-560306-00336-12\n\nДата, до которой необходимо" +
                    " оплатить\n16.03.2026\n\nСумма, подлежащая уплате за" +
                    " совершение нотариального действия (рубли)\n12095,47\n" +
                    "\nРасчетный счет\n358028151020003122\n\nБИК\n" +
                    "544525593\n\nКорреспондентский счёт\n" +
                    "3610181020700000523\n" +
                    "\nНаименование банка\nАО \"АЛЬФА-БАНК\"\n\n" +
                    "Фамилия ВРИО\n" +
                    "Шишкин\n\nИмя ВРИО\nЛи\n\nОтчество ВРИО\n" +
                    "Минулл\n" +
                    "\nИНН ВРИО\n120205595002\n\n")
            page.get_by_role("button", name="Сохранить").click()

        with allure.step("Ожидание успешного сохранения" +
                         " данных подачи документов"):
            expect(page.locator("fnip-button").filter(
                has_text="Указать данные по подаче документов")).to_be_visible(
                    timeout=380000)
            expect(
                page.get_by_text("Операция выполнена успешно. Статус изменен")
                ).to_be_visible(
                    timeout=380000)

        with allure.step("Подтверждение оплаты пошлины"):
            page.get_by_text("Подтвердить оплату пошлины").click()
            page.locator(
                "#cdk-dialog-1 input[type='file']").set_input_files(
                    generate_pdf(2))
            page.get_by_role("button", name="Сохранить").click()

        with allure.step("Указание реквизитов ИНН"):
            page.get_by_text("Ожидание реквизитов ИНН").click()
            page.get_by_role("button", name="Указать реквизиты ИНН").click()
            page.get_by_role("textbox", name="Дата получения ИНН *").click()
            page.get_by_role("button", name="Предыдущий").click()
            page.get_by_text("1", exact=True).first.click()
            page.get_by_role("textbox", name="Реквизиты ИНН *").click()
            page.get_by_role("textbox", name="Реквизиты ИНН *").fill(
                "11233211231")
            page.get_by_role("button", name="Сохранить").click()

        with allure.step("Переход к исполнительному производству"):
            page.locator("span").filter(
                has_text="Исполнительное производство").click()

    @allure.title("Бизнес процесс по ИНН - ошибка ЦФТ")
    @allure.description(
        "Тест проверяет отображение ошибки ЦФТ при работе с ИНН")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.nei
    @pytest.mark.parametrize('username, password', [
        (admin_email, admin_password)])
    @pytest.mark.skip(
        reason="Отключена отправка платёжки в ЦФТ, все запросы успешные")
    def test_process_nei_error_cft(self,
                                   page: Page,
                                   username: str,
                                   password: str):
        direction = DirectionMetods(page, url)
        page.set_default_timeout(60000)

        with allure.step("Получение токена и загрузка миграции"):
            # Запросы для генерации и загрузки досье в систему
            token = direction.get_token()
            contractNumber, credit_id = direction.post_uploadMigration(
                token,
                person_id=1)

        with allure.step(f"Поиск контракта по номеру: {contractNumber}"):
            query = {"contractNumber": f"{contractNumber}"}
            json_data = direction.get_contracts(token, query_params=query)

        with allure.step("Валидация JSON и получение contract_id"):
            # Валидируем JSON и получаем contract_id для запуска процесса
            contract_id, person_id = (
                direction.validation_json_to_id_number_contract(
                    json_data,
                    contractNumber))

        with allure.step("Создание JudicialWork и запуск workflow НЕИ"):
            nei_id = direction.post_JudicialWork(
                token, contractId=contract_id)
            direction.start_workflow_nei(token,
                                         contractId=contract_id,
                                         neiId=nei_id)

        with allure.step("Формирование ссылки для открытия досье:" +
                         f" person_id={person_id}, contract_id={contract_id}"):
            # Формируем ссылку для открытия досье с contract_id, person_id
            contract_url = (f"{base_url}/crm-direction/contracts/" +
                            f"client/{person_id}/contract/{contract_id}")

        with allure.step("Переход по URL и авторизация UI"):
            direction.go_to(contract_url)
            expect(direction.page).to_have_url(f"{login_url}")
            direction.login(username, password)
            expect(page.locator(
                "fnip-toolbar").get_by_text("CRM direction")).to_be_visible()

        with allure.step(f"Поиск контракта {contractNumber} в списке"):
            page.get_by_role("link").nth(4).click()
            page.get_by_role(
                "textbox", name="Номер кредитного договора").click()
            page.get_by_role(
                "textbox", name="Номер кредитного договора").fill(
                    f"{contractNumber}")
            expect(page.locator(".t-tag > .t-icon > .t-svg")).to_be_visible()
            page.locator(".t-tag > .t-icon > .t-svg").click()
            page.get_by_role("link").filter(
                has_text=re.compile(r"^$")).nth(4).click()

        with allure.step("Подача документов нотариусу (приводит к ошибке)"):
            page.get_by_text("Подача документов нотариусу").first.click()
            page.get_by_role("button",
                             name="Указать данные по подаче документов"
                             ).click()
            page.get_by_role("textbox", name="Сумма задолженности *").click()
            page.get_by_role("textbox", name="Сумма задолженности *").fill(
                    "123123123")
            page.locator(".t-box > .t-content").click()
            page.get_by_role(
                "textbox", name="Информация о платеже из ЛК нотариата").click()
            page.get_by_role(
                "textbox",
                name="Информация о платеже из ЛК нотариата").fill(
                    "Номер заявления\n01-260306-00326-02\n\n" +
                    "ФИО нотариуса\nВасильев Иван Васильевич\n\n" +
                    "Адрес нотариуса\n353130, Респ Башкортостан," +
                    " г Стерлитамак, ул Суханова, д 22б\n\n" +
                    "ИНН нотариуса\n027711925947\n\nНазначение платежа\n" +
                    "Оплата нотариального действия - Совершение удалённо" +
                    " исполнительной надписи о взыскании денежных сумм" +
                    " или истребовании имущества от должника по заявлению" +
                    " №122-260306-40326-32\n\nДата, до которой необходимо" +
                    " оплатить\n16.03.2026\n\nСумма, подлежащая уплате за" +
                    " совершение нотариального действия (рубли)\n12095,47\n" +
                    "\nРасчетный счет\n42102810621020003421\n\nБИК\n" +
                    "045522591\n\nКорреспондентский счёт\n" +
                    "40121810200000000591\n" +
                    "\nНаименование банка\nАО \"АЛЬФА-БАНК\"\n\n" +
                    "Фамилия ВРИО\n" +
                    "Шишкин\n\nИмя ВРИО\nВладимир\n\nОтчество ВРИО\n" +
                    "Минулл\n" +
                    "\nИНН ВРИО\n320205195022\n\n")
            page.get_by_role("button", name="Сохранить").click()

        with allure.step("Ожидание ошибки выполнения операции"):
            page.locator("fnip-button").filter(
                has_text="Указать данные по подаче документов").click()
            expect(
                page.get_by_text(
                    "Ошибка выполнения операции")).to_be_visible(
                    timeout=380000)
