import pandas as pd
import os
from datetime import datetime
import xml.etree.ElementTree as ET


def generate_excel_file_with_date(type):
    """Создает Excel файл и сохраняет в Pages/files"""

    # Проверка для типа InclusionDebtorsToDebtCollectorList2
    if type == "InclusionDebtorsToDebtCollectorList2":

        data = {
            "Заемщик гражданин РФ": ["Да", "Да"],
            "Фамилия заемщика": ["Стрельцов", "Пушкин"],
            "Имя заемщика": ["Михаил", "Иван"],
            "Отчество заемщика": ["Васильевич", "Григорьевич"],
            "ИНН заемщика": ["235001638760", "385608472414"],
            "Тип документа, удостоверяющего личность заемщика": [
                "Паспорт РФ", "Паспорт РФ"],
            "Серия документа, удостоверяющего личность заемщика": [
                "5271", "8175"],
            "Номер документа, удостоверяющего личность заемщика": [
                "175283", "551642"],
            "Номер договора": ["941851", "112374"],
            "Дата договора": ["2024-12-22 00:00:00", "2024-12-25 00:00:00"],
            "Дата передачи представителю Кредитора": [
                "2025-01-22 00:00:00", "2025-01-22 00:00:00"],
            "Наименование представителя Кредитора": [
                "ООО Кредитор", "ООО Кредитор"],
            "ИНН представителя": ["3406028098", "3406028098"],
            "ОГРН представителя": ["8338951901456", "8338951901456"],
            "Адрес местонахождения представителя": [
                "620146,Екатеринбург, ул.Академика Бардина, д.48а, кв. 151",
                "620146,Екатеринбург, ул.Академика Бардина, д.48а, кв. 151"
            ],
            "Почтовый адрес представителя": [
                "620146,Екатеринбург, ул.Академика Бардина, д.48а, кв. 151",
                "620146,Екатеринбург, ул.Академика Бардина, д.48а, кв. 151"
            ],
            "Электронная почта представителя": [
                "credit.creditor@mail.com", "credit.creditor@mail.com"],
            "Телефонный номер представителя": [
                "+7(912)6630887", "+7(912)6630887"]
        }

        df = pd.DataFrame(data)

    # Проверка для типа DebtCollectors.Participants.Company
    elif type == "DebtCollectors.Participants.Company":

        row_data = {
            "Заемщик гражданин РФ": "Да",
            "Фамилия заемщика": "ССССССС",
            "Имя заемщика": "ВВВВВВВ",
            "Отчество заемщика": "ННННННН",
            "ИНН заемщика": "223450631352",
            "Тип документа, удостоверяющего личность заемщика": "Паспорт РФ",
            "Серия документа, удостоверяющего личность заемщика": "1111",
            "Номер документа, удостоверяющего личность заемщика": "111111",
            "Номер договора": "4.0/075901/2024-А",
            "Дата договора": "2026-02-04 00:00:00",
            "Дата перехода права требования иному лицу": "2026-02-04 00:00:00",
            "Тип цессионария": "Юр. Лицо",
            "Имя/Наименование юр. лица цессионария": "НАО ПКО «ПКБ»",
            "Фамилия цессионария": "",
            "Отчество цессионария": "",
            "ИНН цессионария": "2723115222",
            "ОГРН цессионария": "1092723000446",
            "Адрес местонахождения цессионария": (
                "108811, г. Москва, км. 22-й (Киевское ш.), домовл.6, стр.1"),
            "Почтовый адрес цессионария": (
                "108811, г. Москва, км. 22-й (Киевское ш.), домовл.6, стр.1"),
            "Электронная почта цессионария": "test@pkbonline.ru",
            "Телефонный номер цессионария": "8(800)2344004",
            "Наименование страны регистрации компании цессионария": "",
            "Регистрационный номер компании-нерезидента" +
            " цессионария в стране регистрации": "",
            "Номер налогоплательщика (аналог ИНН) компании-нерезидента" +
            " цессионария в стране регистрации": ""
        }

        df = pd.DataFrame([row_data])

    # Проверка для типа DebtCollectors.Participants.Person
    elif type == "DebtCollectors.Participants.Person":

        row_data = {
            "Заемщик гражданин РФ": "Да",
            "Фамилия заемщика": "ССССССС",
            "Имя заемщика": "ВВВВВВВ",
            "Отчество заемщика": "ННННННН",
            "ИНН заемщика": "223450631352",
            "Тип документа, удостоверяющего личность заемщика": "Паспорт РФ",
            "Серия документа, удостоверяющего личность заемщика": "1111",
            "Номер документа, удостоверяющего личность заемщика": "111111",
            "Номер договора": "4.0/075901/2024-А",
            "Дата договора": "2026-02-04 00:00:00",
            "Дата перехода права требования иному лицу": "2026-02-04 00:00:00",
            "Тип цессионария": "Физ. лицо",
            "Имя/Наименование юр. лица цессионария": "Имя ИП",
            "Фамилия цессионария": "Фамилия ИП",
            "Отчество цессионария": "",
            "ИНН цессионария": "235001638760",
            "ОГРН цессионария": "1092723000446",
            "Адрес местонахождения цессионария": (
                "108811, г. Москва, км. 22-й (Киевское ш.), домовл.6, стр.1"),
            "Почтовый адрес цессионария": (
                "108811, г. Москва, км. 22-й (Киевское ш.), домовл.6, стр.1"),
            "Электронная почта цессионария": "test@pkbonline.ru",
            "Телефонный номер цессионария": "8(800)2344004",
            "Наименование страны регистрации компании цессионария": "",
            "Регистрационный номер компании-нерезидента" +
            " цессионария в стране регистрации": "",
            "Номер налогоплательщика (аналог ИНН) компании-нерезидента" +
            " цессионария в стране регистрации": ""
        }

        df = pd.DataFrame([row_data])

    # Проверка для типа DebtCollectors.Participants.NonResidentCompany
    elif type == "DebtCollectors.Participants.NonResidentCompany":

        row_data = {
            "Заемщик гражданин РФ": "Да",
            "Фамилия заемщика": "ССССССС",
            "Имя заемщика": "ВВВВВВВ",
            "Отчество заемщика": "ННННННН",
            "ИНН заемщика": "223450631352",
            "Тип документа, удостоверяющего личность заемщика": "Паспорт РФ",
            "Серия документа, удостоверяющего личность заемщика": "1111",
            "Номер документа, удостоверяющего личность заемщика": "111111",
            "Номер договора": "4.0/075901/2024-А",
            "Дата договора": "2026-02-04 00:00:00",
            "Дата перехода права требования иному лицу": "2026-02-04 00:00:00",
            "Тип цессионария": "Компания-нерезидент",
            "Имя/Наименование юр. лица цессионария": "Имя ИП",
            "Фамилия цессионария": "",
            "Отчество цессионария": "",
            "Адрес местонахождения цессионария": (
                "108811, г. Москва, км. 22-й (Киевское ш.), домовл.6, стр.1"),
            "Почтовый адрес цессионария": (
                "108811, г. Москва, км. 22-й (Киевское ш.), домовл.6, стр.1"),
            "Электронная почта цессионария": "test@pkbonline.ru",
            "Телефонный номер цессионария": "8(800)2344004",
            "Наименование страны регистрации компании цессионария": "АЛЖИР",
            "Регистрационный номер компании-нерезидента" +
            " цессионария в стране регистрации": "2130213500",
            "Номер налогоплательщика (аналог ИНН) компании-нерезидента" +
            " цессионария в стране регистрации": "2130213500"
        }

        df = pd.DataFrame([row_data])

    # Проверка для типа DebtCollectors.Participants.IndividualEntrepreneur
    elif type == "DebtCollectors.Participants.IndividualEntrepreneur":

        row_data = {
            "Заемщик гражданин РФ": "Да",
            "Фамилия заемщика": "ССССССС",
            "Имя заемщика": "ВВВВВВВ",
            "Отчество заемщика": "ННННННН",
            "ИНН заемщика": "223450631352",
            "Тип документа, удостоверяющего личность заемщика": "Паспорт РФ",
            "Серия документа, удостоверяющего личность заемщика": "1111",
            "Номер документа, удостоверяющего личность заемщика": "111111",
            "Номер договора": "4.0/075901/2024-А",
            "Дата договора": "2026-02-04 00:00:00",
            "Дата перехода права требования иному лицу": "2026-02-04 00:00:00",
            "Тип цессионария": "ИП",
            "Имя/Наименование юр. лица цессионария": "Имя ИП",
            "Фамилия цессионария": "Фамилия ИП",
            "Отчество цессионария": "Отчество ИП",
            "ИНН цессионария": "235001638760",
            "ОГРН цессионария": "1092723000446",
            "Адрес местонахождения цессионария": (
                "108811, г. Москва, км. 22-й (Киевское ш.), домовл.6, стр.1"),
            "Почтовый адрес цессионария": (
                "108811, г. Москва, км. 22-й (Киевское ш.), домовл.6, стр.1"),
            "Электронная почта цессионария": "test@pkbonline.ru",
            "Телефонный номер цессионария": "8(800)2344004",
            "Наименование страны регистрации компании цессионария": "",
            "Регистрационный номер компании-нерезидента" +
            " цессионария в стране регистрации": "",
            "Номер налогоплательщика (аналог ИНН) компании-нерезидента" +
            " цессионария в стране регистрации": ""
        }

        df = pd.DataFrame([row_data])

    else:
        return None

    # Путь к папке Pages/files (относительно текущего файла)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    files_dir = os.path.join(project_dir, "fedresurs_files")

    # Создаем папку если её нет
    os.makedirs(files_dir, exist_ok=True)

    # Имя файла с датой и типом
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    type_short = type.split(".")[-1] if "." in type else type
    filename = f"fedresurs_{type_short}_{date_str}.xlsx"
    filepath = os.path.join(files_dir, filename)

    # Заменяем все пустые значения на пустые строки перед сохранением
    df = df.fillna('')
    df = df.replace([None, float('nan'), pd.NA], '')

    # Для всех строковых колонок гарантируем пустые строки
    for col in df.columns:
        df[col] = df[col].apply(lambda x: '' if pd.isna(x) or x is None else x)

    # Сохраняем в Excel
    df.to_excel(filepath, index=False, sheet_name='Лист1', na_rep='')

    return filepath


def validate_error_column(file_path):
    """Проверяет что последний столбец с данными - 'Error'"""
    df = pd.read_excel(file_path, nrows=1)
    df = df.dropna(axis=1, how='all')  # убираем пустые столбцы
    last_column = str(df.columns[-1]).strip().lower()
    assert last_column == 'errors', \
        f"Последний столбец '{df.columns[-1]}', ожидался 'Errors'"
    return True


def validate_fedresurs_xml(file_path, expected, type):
    """Проверка XML файла Федресурса с ожидаемыми значениями из Excel"""
    # Проверка для типа InclusionDebtorsToDebtCollectorList2
    if type == "InclusionDebtorsToDebtCollectorList2":
        print(f"Выполняется проверка для типа: {type}")
        assert os.path.exists(file_path), "Файл не найден"
        assert os.path.getsize(file_path) > 0, "Файл пустой"

        tree = ET.parse(file_path)
        root = tree.getroot()

        # Проверка типа сообщения
        message = root.find('.//Message')
        assert message.get(
            'Type') == expected.get(
                'messageType'), f"Неверный тип: {message.get('Type')}"

        # Проверка должников
        debtors = root.findall('.//Debtor')
        assert len(
            debtors) == expected.get(
                'recordCount'), f"Количество должников: {len(
                    debtors)}, ожидалось: {expected.get('recordCount')}"

        for i, debtor in enumerate(debtors):
            exp = expected['debtors'][i]

            # Блок Debtor
            assert debtor.findtext(
                'IsRfCitizen', ''
                ) == exp.get('is_rf_citizen', 'true'
                             ), f"{i+1}: Не гражданин РФ"
            assert debtor.findtext(
                'LastName', ''
                ) == exp.get('last_name', ''
                             ), f"{i+1}: Неверная фамилия"
            assert debtor.findtext(
                'FirstName', ''
                ) == exp.get('first_name', ''
                             ), f"{i+1}: Неверное имя"
            assert debtor.findtext(
                'MiddleName', ''
                ) == exp.get('middle_name', ''), f"{i+1}: Неверное отчество"
            assert debtor.findtext(
                'Inn', '') == exp.get(
                    'inn', ''), f"{i+1}: Неверный ИНН"

            # Блок Document
            doc = debtor.find('.//Document')
            assert doc is not None, f"{i+1}: Нет блока Document"
            assert doc.findtext('.//Type/Code', ''
                                ) == exp.get(
                                    'doc_type', 'PassportRf'
                                    ), f"{i+1}: Неверный тип документа"
            assert doc.findtext('Series', ''
                                ) == exp.get('series', ''
                                             ), f"{i+1}: Неверная серия"
            assert doc.findtext('Number', ''
                                ) == exp.get('number', ''
                                             ), f"{i+1}: Неверный номер"

            # Блок Contracts
            contract = debtor.find('.//Contract')
            assert contract is not None, f"{i+1}: Нет блока Contract"
            assert contract.findtext(
                'Number', ''
                ) == exp.get(
                    'contract_number', ''
                    ), f"{i+1}: Неверный номер договора"
            assert contract.findtext(
                'Date', ''
                ) == exp.get(
                    'contract_date', ''
                    ), f"{i+1}: Неверная дата договора"
            assert contract.findtext(
                './/InvolvementInfo/DateBegin', ''
                ) == exp.get(
                    'involvement_date', ''
                    ), f"{i+1}: Неверная дата передачи"

        print(f"✓ Все проверки пройдены! Должников: {len(debtors)}")
        return True

    # Проверка для типа DebtCollectors.Participants.Company
    elif type == "DebtCollectors.Participants.Company":
        print(f"Выполняется проверка для типа: {type}")

        assert os.path.exists(file_path), "Файл не найден"
        assert os.path.getsize(file_path) > 0, "Файл пустой"

        tree = ET.parse(file_path)
        root = tree.getroot()

        # Проверка типа сообщения
        message = root.find('.//Message')
        assert message.get(
            'Type') == expected.get(
                'messageType'
                ), f"Неверный тип: {message.get('Type')}"

        # Проверка должников
        debtors = root.findall('.//Debtor')
        assert len(debtors) == expected.get(
            'recordCount'), f"Количество должников: {
                len(debtors)}, ожидалось: {
                    expected.get('recordCount')}"

        for i, debtor in enumerate(debtors):
            exp = expected['debtors'][i]

            # Блок Debtor
            assert debtor.findtext(
                'IsRfCitizen', ''
                ) == exp.get(
                    'is_rf_citizen', 'true'
                    ), f"{i+1}: Не гражданин РФ"
            assert debtor.findtext(
                'LastName', ''
                ) == exp.get(
                    'last_name', ''
                    ), f"{i+1}: Неверная фамилия"
            assert debtor.findtext(
                'FirstName', ''
                ) == exp.get(
                    'first_name', ''
                    ), f"{i+1}: Неверное имя"
            assert debtor.findtext(
                'MiddleName', ''
                ) == exp.get(
                    'middle_name', ''
                    ), f"{i+1}: Неверное отчество"
            assert debtor.findtext(
                'Inn', ''
                ) == exp.get(
                    'inn', ''
                    ), f"{i+1}: Неверный ИНН"

            # Блок Document
            doc = debtor.find('.//Document')
            assert doc is not None, f"{i+1}: Нет блока Document"
            assert doc.findtext(
                './/Type/Code', ''
                ) == exp.get(
                    'doc_type', 'PassportRf'
                    ), f"{i+1}: Неверный тип документа"
            assert doc.findtext(
                'Series', ''
                ) == exp.get(
                    'series', ''
                    ), f"{i+1}: Неверная серия"
            assert doc.findtext(
                'Number', ''
                ) == exp.get(
                    'number', ''
                    ), f"{i+1}: Неверный номер"

            # Блок Contracts
            contract = debtor.find('.//Contract')
            assert contract is not None, f"{i+1}: Нет блока Contract"
            assert contract.findtext('Number', '') == exp.get(
                'contract_number', ''), f"{i+1}: Неверный номер договора"
            assert contract.findtext('Date', '') == exp.get(
                'contract_date', ''), f"{i+1}: Неверная дата договора"
            assert contract.findtext(
                './/InvolvementInfo/DateBegin', '') == exp.get(
                    'involvement_date', ''), f"{i+1}: Неверная дата передачи"

            # Блок Assignee (дополнительная проверка для этого типа)
            assignee = root.find('.//Assignee')
            assert assignee is not None, f"{i+1}: Нет блока Assignee"
            assert assignee.findtext(
                'FullName', ''
                ) == exp.get(
                    'assignee_full_name', ''
                    ), f"{i+1}: Неверное имя/наименование цессионария"
            assert assignee.findtext(
                'Inn', ''
                ) == exp.get(
                    'assignee_inn', ''
                    ), f"{i+1}: Неверный ИНН цессионария"
            assert assignee.findtext(
                'Ogrn', ''
                ) == exp.get(
                    'assignee_ogrn', ''
                    ), f"{i+1}: Неверный ОГРНИП цессионария"
            assert assignee.findtext(
                'PostAddress', ''
                ) == exp.get(
                    'assignee_post_address', ''
                    ), f"{i+1}: Неверный почтовый адрес цессионария"
            assert assignee.findtext(
                'Email', ''
                ) == exp.get(
                    'assignee_email', ''
                    ), f"{i+1}: Неверный email цессионария"
            assert assignee.findtext(
                'Phone', ''
                ) == exp.get(
                    'assignee_phone', ''
                    ), f"{i+1}: Неверный телефон цессионария"

        print(f"✓ Все проверки пройдены! Должников: {len(debtors)}")
        return True

    # Проверка для типа DebtCollectors.Participants.Person
    elif type == "DebtCollectors.Participants.Person":
        print(f"Выполняется проверка для типа: {type}")

        assert os.path.exists(file_path), "Файл не найден"
        assert os.path.getsize(file_path) > 0, "Файл пустой"

        tree = ET.parse(file_path)
        root = tree.getroot()

        # Проверка типа сообщения
        message = root.find('.//Message')
        assert message.get(
            'Type') == expected.get(
                'messageType'), f"Неверный тип: {message.get('Type')}"

        # Проверка должников
        debtors = root.findall('.//Debtor')
        assert len(debtors) == expected.get(
            'recordCount'), f"Количество должников: {
                len(debtors)}, ожидалось: {expected.get('recordCount')}"

        for i, debtor in enumerate(debtors):
            exp = expected['debtors'][i]

            # Блок Debtor
            assert debtor.findtext(
                'IsRfCitizen', ''
                ) == exp.get(
                    'is_rf_citizen', 'true'), f"{i+1}: Не гражданин РФ"
            assert debtor.findtext(
                'LastName', '') == exp.get(
                    'last_name', ''), f"{i+1}: Неверная фамилия"
            assert debtor.findtext(
                'FirstName', '') == exp.get(
                    'first_name', ''), f"{i+1}: Неверное имя"
            assert debtor.findtext(
                'MiddleName', '') == exp.get(
                    'middle_name', ''), f"{i+1}: Неверное отчество"
            assert debtor.findtext(
                'Inn', '') == exp.get(
                    'inn', ''), f"{i+1}: Неверный ИНН"

            # Блок Document
            doc = debtor.find('.//Document')
            assert doc is not None, f"{i+1}: Нет блока Document"
            assert doc.findtext(
                './/Type/Code', '') == exp.get(
                    'doc_type', 'PassportRf'), f"{i+1}: Неверный тип документа"
            assert doc.findtext(
                'Series', '') == exp.get('series', ''
                                         ), f"{i+1}: Неверная серия"
            assert doc.findtext(
                'Number', '') == exp.get(
                    'number', ''), f"{i+1}: Неверный номер"

            # Блок Contracts
            contract = debtor.find('.//Contract')
            assert contract is not None, f"{i+1}: Нет блока Contract"
            assert contract.findtext(
                'Number', '') == exp.get('contract_number', ''
                                         ), f"{i+1}: Неверный номер договора"
            assert contract.findtext(
                'Date', '') == exp.get('contract_date', ''
                                       ), f"{i+1}: Неверная дата договора"
            assert contract.findtext(
                './/InvolvementInfo/DateBegin', ''
                ) == exp.get(
                    'involvement_date', ''
                    ), f"{i+1}: Неверная дата передачи"

        print(f"✓ Все проверки пройдены! Должников: {len(debtors)}")
        return True

    # Проверка для типа DebtCollectors.Participants.NonResidentCompany
    elif type == "DebtCollectors.Participants.NonResidentCompany":
        print(f"Выполняется проверка для типа: {type}")

        assert os.path.exists(file_path), "Файл не найден"
        assert os.path.getsize(file_path) > 0, "Файл пустой"

        tree = ET.parse(file_path)
        root = tree.getroot()

        # Проверка типа сообщения
        message = root.find('.//Message')
        assert message.get(
            'Type') == expected.get(
                'messageType'), f"Неверный тип: {message.get('Type')}"

        # Проверка должников
        debtors = root.findall('.//Debtor')
        assert len(
            debtors) == expected.get(
                'recordCount'), f"Количество должников: {len(
                    debtors)}, ожидалось: {expected.get('recordCount')}"

        for i, debtor in enumerate(debtors):
            exp = expected['debtors'][i]

            # Блок Debtor
            assert debtor.findtext(
                'IsRfCitizen', ''
                ) == exp.get(
                    'is_rf_citizen', 'true'), f"{i+1}: Не гражданин РФ"
            assert debtor.findtext(
                'LastName', ''
                ) == exp.get('last_name', ''), f"{i+1}: Неверная фамилия"
            assert debtor.findtext(
                'FirstName', ''
                ) == exp.get('first_name', ''), f"{i+1}: Неверное имя"
            assert debtor.findtext(
                'MiddleName', ''
                ) == exp.get('middle_name', ''), f"{i+1}: Неверное отчество"
            assert debtor.findtext(
                'Inn', ''
                ) == exp.get('inn', ''), f"{i+1}: Неверный ИНН"

            # Блок Document
            doc = debtor.find('.//Document')
            assert doc is not None, f"{i+1}: Нет блока Document"
            assert doc.findtext(
                './/Type/Code', ''
                ) == exp.get(
                    'doc_type', 'PassportRf'), f"{i+1}: Неверный тип документа"
            assert doc.findtext(
                'Series', ''
                ) == exp.get(
                    'series', ''), f"{i+1}: Неверная серия"
            assert doc.findtext(
                'Number', ''
                ) == exp.get('number', ''), f"{i+1}: Неверный номер"

            # Блок Contracts
            contract = debtor.find('.//Contract')
            assert contract is not None, f"{i+1}: Нет блока Contract"
            assert contract.findtext(
                'Number', ''
                ) == exp.get(
                    'contract_number', ''
                    ), f"{i+1}: Неверный номер договора"
            assert contract.findtext(
                'Date', ''
                ) == exp.get(
                    'contract_date', ''
                    ), f"{i+1}: Неверная дата договора"
            assert contract.findtext(
                './/InvolvementInfo/DateBegin', ''
                ) == exp.get(
                    'involvement_date', ''
                    ), f"{i+1}: Неверная дата передачи"

            # Блок Assignee (дополнительная проверка для нерезидента-компании)
            assignee = root.find('.//Assignee')
            assert assignee is not None, f"{i+1}: Нет блока Assignee"
            assert assignee.findtext(
                'PostAddress', ''
                ) == exp.get(
                    'assignee_post_address', ''
                    ), f"{i+1}: Неверный почтовый адрес цессионария"
            assert assignee.findtext(
                'Email', ''
                ) == exp.get(
                    'assignee_email', ''
                    ), f"{i+1}: Неверный email цессионария"
            assert assignee.findtext(
                'Phone', ''
                ) == exp.get(
                    'assignee_phone', ''
                    ), f"{i+1}: Неверный телефон цессионария"
            assert assignee.findtext(
                'Regnum', ''
                ) == exp.get(
                    'assignee_regnum', ''
                    ), (f"{i+1}: Неверный регистрационный" +
                        "номер компании-нерезидента")
            assert assignee.findtext(
                'Country', ''
                ) == exp.get(
                    'assignee_country', ''
                    ), f"{i+1}: Неверное наименование страны регистрации"
        return True
    # Проверка для типа DebtCollectors.Participants.IndividualEntrepreneur
    elif type == "DebtCollectors.Participants.IndividualEntrepreneur":
        print(f"Выполняется проверка для типа: {type}")

        assert os.path.exists(file_path), "Файл не найден"
        assert os.path.getsize(file_path) > 0, "Файл пустой"

        tree = ET.parse(file_path)
        root = tree.getroot()

        # Проверка типа сообщения
        message = root.find('.//Message')
        assert message.get(
            'Type') == expected.get(
                'messageType'), f"Неверный тип: {message.get('Type')}"

        # Проверка должников
        debtors = root.findall('.//Debtor')
        assert len(
            debtors) == expected.get(
                'recordCount'), f"Количество должников: {len(
                    debtors)}, ожидалось: {expected.get('recordCount')}"

        for i, debtor in enumerate(debtors):
            exp = expected['debtors'][i]

            # Блок Debtor
            assert debtor.findtext(
                'IsRfCitizen', '') == exp.get(
                    'is_rf_citizen', 'true'), f"{i+1}: Не гражданин РФ"
            assert debtor.findtext(
                'LastName', '') == exp.get(
                    'last_name', ''), f"{i+1}: Неверная фамилия"
            assert debtor.findtext(
                'FirstName', '') == exp.get(
                    'first_name', ''), f"{i+1}: Неверное имя"
            assert debtor.findtext(
                'MiddleName', '') == exp.get(
                    'middle_name', ''), f"{i+1}: Неверное отчество"
            assert debtor.findtext(
                'Inn', '') == exp.get(
                    'inn', ''), f"{i+1}: Неверный ИНН"

            # Блок Document
            doc = debtor.find('.//Document')
            assert doc is not None, f"{i+1}: Нет блока Document"
            assert doc.findtext(
                './/Type/Code', '') == exp.get(
                    'doc_type', 'PassportRf'), f"{i+1}: Неверный тип документа"
            assert doc.findtext(
                'Series', '') == exp.get(
                    'series', ''), f"{i+1}: Неверная серия"
            assert doc.findtext(
                'Number', '') == exp.get(
                    'number', ''), f"{i+1}: Неверный номер"

            # Блок Contracts
            contract = debtor.find('.//Contract')
            assert contract is not None, f"{i+1}: Нет блока Contract"
            assert contract.findtext(
                'Number', '') == exp.get(
                    'contract_number', ''), f"{i+1}: Неверный номер договора"
            assert contract.findtext(
                'Date', '') == exp.get(
                    'contract_date', ''), f"{i+1}: Неверная дата договора"
            assert contract.findtext(
                './/InvolvementInfo/DateBegin', '') == exp.get(
                    'involvement_date', ''), f"{i+1}: Неверная дата передачи"

            # Блок Assignee (дополнительная проверка для ИП)
            assignee = root.find('.//Assignee')
            assert assignee is not None, f"{i+1}: Нет блока Assignee"
            assert assignee.findtext(
                'FirstName', '') == exp.get(
                    'assignee_first_name', ''
                    ), f"{i+1}: Неверное имя/наименование цессионария"
            assert assignee.findtext(
                'LastName', '') == exp.get(
                    'assignee_last_name', ''
                    ), f"{i+1}: Неверная фамилия цессионария"
            assert assignee.findtext(
                'MiddleName', '') == exp.get(
                    'assignee_middle_name', ''
                    ), f"{i+1}: Неверное отчество цессионария"
            assert assignee.findtext(
                'Inn', '') == exp.get(
                    'assignee_inn', ''), f"{i+1}: Неверный ИНН цессионария"
            assert assignee.findtext(
                'Ogrnip', '') == exp.get(
                    'assignee_ogrn', ''), f"{i+1}: Неверный ОГРНИП цессионария"
            assert assignee.findtext(
                'PostAddress', '') == exp.get(
                    'assignee_post_address', ''
                    ), f"{i+1}: Неверный почтовый адрес цессионария"
            assert assignee.findtext(
                'Email', '') == exp.get(
                    'assignee_email', ''), f"{i+1}: Неверный email цессионария"
            assert assignee.findtext(
                'Phone', '') == exp.get(
                    'assignee_phone', ''
                    ), f"{i+1}: Неверный телефон цессионария"

        print(f"✓ Все проверки пройдены! Должников: {len(debtors)}")
        return True

    else:
        print(f"Неизвестный тип проверки: {type}")
        return False


def get_expected_values_from_excel(file_path, type):
    """Читает Excel файл и возвращает ожидаемые значения для проверки XML"""

    df = pd.read_excel(file_path)

    # Для типа InclusionDebtorsToDebtCollectorList2
    # (Привлечение кредитором представителя)
    if type == "InclusionDebtorsToDebtCollectorList2":
        expected = {
            'messageType': 'InclusionDebtorsToDebtCollectorList2',
            'recordCount': len(df),
            'assignee_name': df.iloc[0][
                'Наименование представителя Кредитора'],
            'assignee_inn': str(df.iloc[0][
                'ИНН представителя']),
            'assignee_ogrn': str(df.iloc[0][
                'ОГРН представителя']),
            'assignee_post_address': df.iloc[0][
                'Почтовый адрес представителя'],
            'assignee_email': df.iloc[0][
                'Электронная почта представителя'],
            'assignee_phone': str(df.iloc[0][
                'Телефонный номер представителя']),
            'debtors': []
        }

        for _, row in df.iterrows():
            # Обработка даты договора
            contract_date = row['Дата договора']
            if pd.notna(contract_date):
                if hasattr(contract_date, 'strftime'):
                    contract_date = contract_date.strftime('%Y-%m-%d')
                else:
                    contract_date = str(contract_date).split()[0]

            # Обработка даты передачи
            involvement_date = row['Дата передачи представителю Кредитора']
            if pd.notna(involvement_date):
                if hasattr(involvement_date, 'strftime'):
                    involvement_date = involvement_date.strftime('%Y-%m-%d')
                else:
                    involvement_date = str(involvement_date).split()[0]

            debtor = {
                'is_rf_citizen': 'true' if row[
                    'Заемщик гражданин РФ'] == 'Да' else 'false',
                'last_name': row['Фамилия заемщика'],
                'first_name': row['Имя заемщика'],
                'middle_name': row['Отчество заемщика'],
                'inn': str(row['ИНН заемщика']),
                'doc_type': 'PassportRf' if row[
                    'Тип документа, удостоверяющего личность заемщика'
                    ] == 'Паспорт РФ' else row[
                        'Тип документа, удостоверяющего личность заемщика'],
                'series': str(row[
                    'Серия документа, удостоверяющего личность заемщика']),
                'number': str(row[
                    'Номер документа, удостоверяющего личность заемщика']),
                'contract_number': str(row[
                    'Номер договора']),
                'contract_date': contract_date,
                'involvement_date': involvement_date
            }
            expected['debtors'].append(debtor)

    # Для типа IndividualEntrepreneur (отдельная обработка)
    elif type == "DebtCollectors.Participants.IndividualEntrepreneur":
        expected = {
            'messageType': 'AssignmentOfClaim',
            'recordCount': len(df),
            'debtors': []
        }

        for _, row in df.iterrows():
            # Обработка даты договора
            contract_date = row['Дата договора']
            if pd.notna(contract_date):
                if hasattr(contract_date, 'strftime'):
                    contract_date = contract_date.strftime('%Y-%m-%d')
                else:
                    contract_date = str(contract_date).split()[0]

            # Обработка даты перехода права требования
            assignment_date = row['Дата перехода права требования иному лицу']
            if pd.notna(assignment_date):
                if hasattr(assignment_date, 'strftime'):
                    assignment_date = assignment_date.strftime('%Y-%m-%d')
                else:
                    assignment_date = str(assignment_date).split()[0]

            debtor = {
                'is_rf_citizen': 'true' if row['Заемщик гражданин РФ'
                                               ] == 'Да' else 'false',
                'last_name': str(row['Фамилия заемщика']),
                'first_name': str(row['Имя заемщика']),
                'middle_name': str(row['Отчество заемщика']),
                'inn': str(row['ИНН заемщика']),
                'doc_type': 'PassportRf' if row[
                    'Тип документа, удостоверяющего личность заемщика'
                    ] == 'Паспорт РФ' else str(row[
                        'Тип документа, удостоверяющего личность заемщика']),
                'series': str(row[
                    'Серия документа, удостоверяющего личность заемщика']),
                'number': str(row[
                    'Номер документа, удостоверяющего личность заемщика']),
                'contract_number': str(row['Номер договора']),
                'contract_date': contract_date,
                'assignment_date': assignment_date,
                'assignee_type': str(row.get('Тип цессионария', '')),
                'assignee_first_name': str(row.get(
                    'Имя/Наименование юр. лица цессионария', '')),
                'assignee_last_name': str(row.get(
                    'Фамилия цессионария', '')),
                'assignee_middle_name': str(row.get(
                    'Отчество цессионария', '')),
                'assignee_inn': str(row.get(
                    'ИНН цессионария', '')),
                'assignee_ogrn': str(row.get(
                    'ОГРН цессионария', '')),
                'assignee_address': str(row.get(
                    'Адрес местонахождения цессионария', '')),
                'assignee_post_address': str(row.get(
                    'Почтовый адрес цессионария', '')),
                'assignee_email': str(row.get(
                    'Электронная почта цессионария', '')),
                'assignee_phone': str(row.get(
                    'Телефонный номер цессионария', '')),
                'assignee_country': str(row.get(
                    'Наименование страны регистрации компании цессионария', ''
                    )),
                'assignee_regnum': str(
                    row.get(
                        'Регистрационный номер компании-нерезидента' +
                        ' цессионария в стране регистрации', '')),
                'assignee_tax_number': str(row.get(
                    'Номер налогоплательщика (аналог ИНН) ' +
                    'компании-нерезидента цессионария в стране регистрации', ''
                    ))
            }
            expected['debtors'].append(debtor)

    # Для остальных типов цессии (Company, Person, NonResidentCompany)
    else:
        expected = {
            'messageType': 'AssignmentOfClaim',
            'recordCount': len(df),
            'debtors': []
        }

        for _, row in df.iterrows():
            # Обработка даты договора
            contract_date = row['Дата договора']
            if pd.notna(contract_date):
                if hasattr(contract_date, 'strftime'):
                    contract_date = contract_date.strftime('%Y-%m-%d')
                else:
                    contract_date = str(contract_date).split()[0]

            # Обработка даты перехода права требования
            assignment_date = row['Дата перехода права требования иному лицу']
            if pd.notna(assignment_date):
                if hasattr(assignment_date, 'strftime'):
                    assignment_date = assignment_date.strftime('%Y-%m-%d')
                else:
                    assignment_date = str(assignment_date).split()[0]

            debtor = {
                'is_rf_citizen': 'true' if row[
                    'Заемщик гражданин РФ'] == 'Да' else 'false',
                'last_name': str(row['Фамилия заемщика']),
                'first_name': str(row['Имя заемщика']),
                'middle_name': str(row['Отчество заемщика']),
                'inn': str(row['ИНН заемщика']),
                'doc_type': 'PassportRf' if row[
                    'Тип документа, удостоверяющего личность заемщика'
                    ] == 'Паспорт РФ' else str(row[
                        'Тип документа, удостоверяющего личность заемщика']),
                'series': str(row[
                    'Серия документа, удостоверяющего личность заемщика']),
                'number': str(row[
                    'Номер документа, удостоверяющего личность заемщика']),
                'contract_number': str(row['Номер договора']),
                'contract_date': contract_date,
                'assignment_date': assignment_date,
                'assignee_type': str(row.get('Тип цессионария', '')),
                'assignee_full_name': str(row.get(
                    'Имя/Наименование юр. лица цессионария', '')),
                'assignee_last_name': str(row.get(
                    'Фамилия цессионария', '')),
                'assignee_middle_name': str(row.get(
                    'Отчество цессионария', '')),
                'assignee_inn': str(row.get(
                    'ИНН цессионария', '')),
                'assignee_ogrn': str(row.get(
                    'ОГРН цессионария', '')),
                'assignee_address': str(row.get(
                    'Адрес местонахождения цессионария', '')),
                'assignee_post_address': str(row.get(
                    'Почтовый адрес цессионария', '')),
                'assignee_email': str(row.get(
                    'Электронная почта цессионария', '')),
                'assignee_phone': str(row.get(
                    'Телефонный номер цессионария', '')),
                'assignee_country': str(row.get(
                    'Наименование страны регистрации компании цессионария', ''
                    )),
                'assignee_regnum': str(row.get(
                    'Регистрационный номер компании-нерезидента цессионария' +
                    ' в стране регистрации', '')),
                'assignee_tax_number': str(row.get(
                    'Номер налогоплательщика (аналог ИНН) ' +
                    'компании-нерезидента цессионария в стране регистрации', ''
                    ))
            }
            expected['debtors'].append(debtor)

    return expected
