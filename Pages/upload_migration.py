import random
import string
import csv
import pytest
import datetime
from .data_templates import (
    list_field_names,
    dict_persons,
    dict_guarantors,
    dict_coborrowers,
    surnames_list)
from dotenv import load_dotenv
from .main_page import MainPage

load_dotenv(override=True)


class UploadMigrationMetods(MainPage):
    """Класс методов для UploadMigrationMetods"""
    def __init__(self, page, url=None, timeout=10):
        super().__init__(page, url, timeout)
        self.generated_data = {}

    def random_string(self, length=10):
        """Генерирует строку указанной длины из
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'"""
        letters = string.ascii_letters
        return ''.join(random.choices(letters, k=length))

    def random_number(self, length=10):
        """Генерирует номер указанной длины с +7"""
        number = string.digits
        return '+7' + ''.join(random.choices(number, k=length))

    def random_id_credit(self, length=12):
        """Генерирует id кредита указанной длины"""
        number = string.digits
        return ''.join(random.choices(number, k=length))

    def random_sum_credit(self):
        """Генерирует сумму кредита"""
        part1 = f"{random.randint(1000, 9999)}"
        part2 = f"{random.randint(1, 99)}"
        return f"{part1}.{part2}"

    def random_pene_credit(self):
        """Генерирует сумму кредита"""
        part1 = f"{random.randint(100, 990)}"
        part2 = f"{random.randint(1, 99)}"
        return f"{part1}.{part2}"

    def random_number_contract_to_template(self):
        part1 = f"{random.randint(10, 99)}"
        part2 = f"{random.randint(0, 9999):04d}"
        part3 = f"{random.randint(0, 9)}{random.choice('abcdef')}"
        part4 = f"{random.randint(0, 9999999999):010d}"
        return f"{part1}-{part2}-{part3}-{part4}"

    def random_number_contract(self, length=18):
        """Генерирует номер договора указанной длины"""
        number = string.digits
        return ''.join(random.choices(number, k=length))

    def random_numeric_string(self, length=18):
        """Генерирует строку чисел указанной длины"""
        number = string.digits
        return ''.join(random.choices(number, k=length))

    def choose_surname(self, surnames_list=surnames_list):
        """Выбирает случайную фамилию из списка."""
        return random.choice(surnames_list)

    def get_time(sef, params=None):
        """"Возвращает текущее время,
        если не указаны параметры возвращает только Ч:М:С"""
        now = datetime.datetime.now()
        timestamp = now.strftime(
            f'{params if params is not None else "%H-%M-%S"}')
        return timestamp

    def validation_json_to_id_number_contract(
            self, json_data_contract=None,
            number_contract=None,
            override=False):
        """"Метод проверки наличия кредитного договора
        в DIRECTION_CONTRACTS возвращает contract_id
        в случае нахождения"""
        if override is False:
            try:
                all_items = json_data_contract['data']['page']['items']
                for i in range(0, all_items+1):
                    number = json_data_contract['data']['data'][i][(
                        'creditContractNumber')]
                    if number == number_contract:
                        contract_id = json_data_contract['data']['data'][i][(
                            'id')]
                        person_id = json_data_contract['data']['data'][i][(
                            'person')]['id']
                        return contract_id, person_id
            except (AssertionError, IndexError):
                return pytest.fail(
                        f'Номера кредитного контракта {number_contract} ' +
                        'нет в DIRECTION_CONTRACTS')
        if override is True:
            try:
                person_id = 1
                person_list = list(dict_persons[f'person{person_id}'])
                all_items = json_data_contract['data']['page']['items']
                for i in range(0, all_items+1):
                    number = json_data_contract['data']['data'][i][(
                        'creditContractNumber')]
                    if number == person_list[44]:
                        contract_id = json_data_contract['data']['data'][i][(
                            'id')]
                        return contract_id
            except (AssertionError, IndexError):
                return pytest.fail(
                        f'Номера кредитного контракта {number_contract} ' +
                        'нет в DIRECTION_CONTRACTS')

    def validation_json_to_id_person_id(
            self, json_data_contract=None,
            json_data_person=None,
            number_contract=None):
        """"Метод проверки наличия ID заёмщика
        в DIRECTION_PERSONS возвращает person_id
        в случае нахождения"""
        try:
            person_id = 1
            person_list = list(dict_persons[f'person{person_id}'])
            number_contract = person_list[44]
            all_items = json_data_contract['data']['page']['items']
            all_person = json_data_person['data']['page']['items']
            for i in range(0, all_items+1):
                number = json_data_contract['data']['data'][i][(
                    'creditContractNumber')]
                if number == number_contract:
                    person_id = json_data_contract[(
                        'data')]['data'][i]['person']['id']
                    break
        except (AssertionError, IndexError):
            return pytest.fail(
                    f'Номера кредитного контракта {number_contract} ' +
                    'нет в DIRECTION_CONTRACTS')
        try:
            for x in range(0, all_person+1):
                person = json_data_person['data']['data'][x]['id']
                if person == person_id:
                    return person_id
        except (AssertionError, IndexError):
            return pytest.fail(
                f'ID заёмщика {person_id} ' +
                'нет в DIRECTION_PERSONS')

    def validation_json_JudicialWork(self,
                                     json_contracts=None,
                                     json_judicial=None,
                                     after_post=False,
                                     idCourtDeal=None):
        if after_post is False:
            try:
                all_items_contracts = json_contracts['data']['page']['items']
                all_items_judicial = json_judicial['data']['page']['items']
                for i in range(all_items_contracts + 1):
                    number_contract = json_contracts['data']['data'][i]['id']
                    found = False
                    for x in range(all_items_judicial):
                        number = json_judicial['data']['data'][x]['contractId']
                        if number == number_contract:
                            found = True
                            break
                    if not found:
                        contract_id = number_contract
                        return contract_id
            except (AssertionError, IndexError):
                return pytest.fail(
                        f'Номера кредитного договора {number_contract} ' +
                        'нет в DIRECTION_COURT_DEAL')
        if after_post is True:
            try:
                idCourtDeal = idCourtDeal['data']['data']['id']
                all_items_judicial = json_judicial['data']['page']['items']
                for i in range(all_items_judicial):
                    id = json_judicial['data']['data'][i]['id']
                    if id == idCourtDeal:
                        return True
            except (AssertionError, IndexError):
                return pytest.fail(
                        f'Номера кредитного договора {number_contract} ' +
                        'нет в DIRECTION_COURT_DEAL')

    def scan_contract_data(
            self, json_contract=None):
        """"Метод возвращающий данные по договору и конкретным полям
        из DIRECTION_CONTRACTS принимает json по конкретному json_contract"""
        try:
            creditTotalSum = json_contract['data'][(
                'creditTotalSum')]
            sumAnnuity = json_contract['data'][(
                'sumAnnuity')]
            overdueLoanPrincipal = json_contract[(
                'data')]['overdueLoanPrincipal']
            overdueInterestDebt = json_contract[(
                'data')][('overdueInterestDebt')]
            pene = json_contract[(
                'data')][('pene')]
            courtFee = json_contract[(
                'data')][('courtFee')]
            nonCourtFee = json_contract[(
                'data')][('nonCourtFee')]
            debtSumRub = json_contract[(
                'data')][('debtSumRub')]
            return (creditTotalSum, sumAnnuity,
                    overdueLoanPrincipal,
                    overdueInterestDebt, pene, courtFee, nonCourtFee,
                    debtSumRub)
        except KeyError as e:
            field_name = e.args[0]
            return pytest.fail(f'Поле "{field_name}" не найдено в теле ответа')

    def scan_person_data(
            self, json_person=None):
        """"Метод возвращающий данные по договору и конкретным полям
        из DIRECTION_PERSONS принимает json по конкретному person_id"""
        try:
            max_id_doc = max(json_person['data']['documents'],
                             key=lambda x: x['id'])

            series_doc = max_id_doc['series']
            number_doc = max_id_doc['number']
            issuedBy_doc = max_id_doc['issuedBy']
            issuedDate_doc = max_id_doc['issuedDate']
            placeBirth_doc = max_id_doc['placeBirth']
            registrationAddress = json_person[(
                'data')]['registrationAddress']
            address = json_person['data']['address']
            return (series_doc, number_doc, issuedBy_doc,
                    issuedDate_doc, placeBirth_doc,
                    registrationAddress, address)
        except KeyError as e:
            field_name = e.args[0]
            return pytest.fail(f'Поле "{field_name}" не найдено в теле ответа')

    def scan_guarantor_data(
            self, json_guarantor=None):
        """"Метод возвращающий данные по конкретным полям получителя
        принимает json по конкретному guarantors"""
        try:
            last_guarantor = max(json_guarantor['data'],
                                 key=lambda x: x['id'])

            lastname = last_guarantor['person']['lastName']
            homephone = last_guarantor['person']['homePhone']
            return (lastname, homephone)
        except KeyError as e:
            field_name = e.args[0]
            return pytest.fail(f'Поле "{field_name}" не найдено в теле ответа')

    def scan_coborrower_data(
            self, json_coborrower=None):
        """"Метод возвращающий данные по конкретным полям созаёмщика
        принимает json по конкретному coborrowers"""
        try:
            last_coborrower = max(json_coborrower['data'],
                                  key=lambda x: x['id'])

            lastname = last_coborrower['person']['lastName']
            homephone = last_coborrower['person']['mobilePhone']
            return (lastname, homephone)
        except KeyError as e:
            field_name = e.args[0]
            return pytest.fail(f'Поле "{field_name}" не найдено в теле ответа')

    def validation_json_to_coborrower(
            self, json_coborrower=None,
            credit_id=None):
        """"Метод проверки наличия созаёмщика привязанного к контракту"""
        try:
            credit_id_coborrower = json_coborrower[
                'data'][0]['person']['externalId']
            credit_id_coborrower = credit_id_coborrower.split('#')[0]
            assert credit_id == credit_id_coborrower
        except (AssertionError, IndexError):
            return pytest.fail(
                    'Значение кредитного договора ' +
                    f'у созаёмщика отличается от {credit_id}')

    def validation_json_to_guarantor(
            self, json_guarantor=None,
            credit_id=None):
        """"Метод проверки наличия поручителя привязанного к контракту"""
        try:
            credit_id_guarantor = json_guarantor[
                'data'][0]['person']['externalId']
            credit_id_guarantor = credit_id_guarantor.split('#')[0]
            assert credit_id == credit_id_guarantor
        except (AssertionError, IndexError):
            return pytest.fail(
                    'Значение кредитного договора ' +
                    f'у поручителя отличается от {credit_id}')

    def comparison_contact_data(
            self, first_scan_list=None,
            second_scan_list=None):
        """"Метод сравнивает списки из метода scan_contract_data
        и возвращает True при разных списках и False если значения совпали
        из DIRECTION_CONTRACTS"""
        try:
            assert first_scan_list != second_scan_list
            return True
        except (AssertionError, IndexError):
            return pytest.fail(f'Списки {first_scan_list} и ' +
                               f'{second_scan_list} совпали')

    def comparison_person_data(
            self, first_scan_list=None,
            second_scan_list=None):
        """"Метод сравнивает списки из метода scan_person_data
        и возвращает True при разных списках и False если значения совпали
        из DIRECTION_PERSONS"""
        try:
            assert first_scan_list != second_scan_list
            result = 0
            for i in range(0, len(first_scan_list)):
                if first_scan_list[i] == second_scan_list[i]:
                    result += 1
            assert result == 0
            return True
        except (AssertionError, IndexError):
            return pytest.fail(f'Списки {first_scan_list} и ' +
                               f'{second_scan_list} совпали')

    def comparison_guarantor_data(
            self, first_scan_list=None,
            second_scan_list=None):
        """"Метод сравнивает списки из метода scan_guarantor_data
        и возвращает True при разных списках и False если значения совпали
        из DIRECTION_PERSONS"""
        try:
            result = 0
            for i in range(0, len(first_scan_list)):
                if first_scan_list[i] == second_scan_list[i]:
                    result += 1
            assert result == 0
            return True
        except (AssertionError, IndexError):
            return pytest.fail(f'Списки {first_scan_list} и ' +
                               f'{second_scan_list} совпали')

    def comparison_coborrower_data(
            self, first_scan_list=None,
            second_scan_list=None):
        """"Метод сравнивает списки из метода scan_coborrower_data
        и возвращает True при разных списках и False если значения совпали
        из DIRECTION_PERSONS"""
        try:
            result = 0
            for i in range(0, len(first_scan_list)):
                if first_scan_list[i] == second_scan_list[i]:
                    result += 1
            assert result == 0
            return True
        except (AssertionError, IndexError):
            return pytest.fail(f'Списки {first_scan_list} и ' +
                               f'{second_scan_list} совпали')

    def create_csv_file(self, rows=None,
                        filename='data.csv',
                        fieldnames=list_field_names,
                        person_id=None,
                        override_contract=False,
                        override_person=False,
                        guarantors=False,
                        override_guarantors=False,
                        coborrowers=False,
                        override_coborrowers=False,
                        have_security=True,
                        credit_id=None):
        """Создаёт CSV файл по шаблону столбцов fieldnames
        и заполняет данные по шаблону rows"""
        try:
            override_contract = override_contract
            person_list = list(dict_persons[f'person{person_id}'])
            guarantor_list = list(dict_guarantors[f'guarantor{person_id}'])
            coborrower_list = list(dict_coborrowers[f'coborrower{person_id}'])
            number_contract = self.random_number_contract_to_template()
            if person_id != 1:
                number_contract = person_list[44]
            if have_security is False:
                have_security_ct = ''
                credit_id = credit_id
            else:
                have_security_ct = person_list[22]
                credit_id = self.random_id_credit()
            rows = [{
                        'Номер договора': f'{number_contract}',
                        'Фамилия': f'{person_list[0]}',
                        'Имя': f'{person_list[1]}',
                        'Отчество': f'{person_list[2]}',
                        'Дата начала кредита': '10.11.2024',
                        'Дата рождения заемшика': f'{person_list[3]}',
                        'Место рождения заемщика': f'{person_list[4]}',
                        'Серия паспорта заемщика': f'{person_list[5]}',
                        'Номер паспорта заемщика': f'{person_list[6]}',
                        'Код подразделения выдавшего паспорт': f'{
                            person_list[16]}',
                        'Дата выдачи паспорта заемщика': f'{person_list[7]}',
                        'Кем выдан Паспорт заемщику': f'{person_list[8]}',
                        'Адрес регистрации заемщика': f'{person_list[9]}',
                        # 'Место жительства заемщика': f'{person_list[10]}',
                        'Телефон Мобильный': f'{person_list[11]}',
                        'Кредиты # ID': f'{credit_id}',
                        'Вид кредита': f'{person_list[12]}',
                        'Тип проекта': f'{person_list[13]}',
                        'Сумма выдачи': f'{person_list[15]}',
                        'Валюта кредита': f'{person_list[17]}',
                        'Сумма аннуитета': f'{person_list[18]}',
                        'Дата аннуитета': f'{person_list[19]}',
                        'Подразделение': f'{person_list[20]}',
                        'Залог авто:Модель и марка автомобиля': (
                            f'{person_list[21]}'),
                        'Залог авто: VIN': (
                            f'{have_security_ct}'),
                        'Залог авто: год производства автомобиля': (
                            f'{person_list[23]}'),
                        # 'Залог авто: цвет автомобиля': (
                        #     f'{person_list[24]}'),
                        'Залог авто: номер ПТС': f'{person_list[25]}',
                        'Ссудная задолженность, руб.': (f'{person_list[26]}'),
                        'Просроченная ссудная задолженность, руб.': (
                            f'{person_list[27]}'),
                        'Неучтенные проценты за кредит, руб.': (
                            f'{person_list[28]}'),
                        'Неучтенные проценты (выкупленные), руб': (
                            f'{person_list[29]}'),
                        'Учтенные проценты за кредит, руб': (
                            f'{person_list[30]}'),
                        'Срочные проценты на внебалансе, руб.': (
                            f'{person_list[31]}'),
                        'Просроченная задолженность ' +
                        'по проц. на внебалансе, руб.': f'{person_list[32]}',
                        'Просроченная задолженность по процентам, руб.': (
                            f'{person_list[33]}'),
                        'Просроченные проценты (выкупленные), руб': (
                            f'{person_list[34]}'),
                        'Общая задолженность, руб.': f'{person_list[35]}',
                        'Наличие активированного ДБО': f'{person_list[36]}',
                        'Адрес эл.почты': f'{person_list[37]}',
                        'Признанные штрафы и пени': f'{person_list[38]}',
                        'Присужденная госпошлина': f'{person_list[39]}',
                        'Неприсужденная госпошлина': f'{person_list[40]}',
                        # 'Дата смерти': f'{person_list[41]}',
                        'Срок просрочки по FIFO': f'{person_list[42]}',
                        'Срок просрочки по LIFO': f'{person_list[43]}',
                        'Задолженность по пене за проценты, руб.': (
                            f'{person_list[47]}'),
                        'Актуальная процентная ставка по ОД': 11,
                        'Начальная процентная ставка по ОД': 11,
                        'Задолженность по пене за кредит, руб.': 1000
                        # остальные поля можно оставить пустыми или заполнить
                    }]
            if override_contract and have_security:
                number_contract = f'{person_list[44]}'
                credit_id = person_list[14]
                print('я тут')
                rows_update = {
                        'Номер договора': f'{number_contract}',
                        'Кредиты # ID': f'{credit_id}',
                        'Сумма выдачи': f'{self.random_sum_credit()}',
                        'Валюта кредита': f'{person_list[17]}',
                        'Сумма аннуитета': f'{self.random_pene_credit()}',
                        'Просроченная ссудная задолженность, руб.': (
                            f'{self.random_pene_credit()}'),
                        'Неучтенные проценты за кредит, руб.': (
                            f'{self.random_pene_credit()}'),
                        'Неучтенные проценты (выкупленные), руб': (
                            f'{self.random_pene_credit()}'),
                        'Учтенные проценты за кредит, руб': (
                            f'{self.random_pene_credit()}'),
                        'Срочные проценты на внебалансе, руб.': (
                            f'{self.random_pene_credit()}'),
                        'Просроченная задолженность ' +
                        'по проц. на внебалансе, руб.': (
                            f'{self.random_pene_credit()}'),
                        'Просроченная задолженность по процентам, руб.': (
                            f'{self.random_pene_credit()}'),
                        'Просроченные проценты (выкупленные), руб': (
                            f'{self.random_pene_credit()}'),
                        'Общая задолженность, руб.': (
                            f'{self.random_pene_credit()}'),
                        'Признанные штрафы и пени': (
                            f'{self.random_pene_credit()}'),
                        'Присужденная госпошлина': (
                            f'{self.random_pene_credit()}'),
                        'Неприсужденная госпошлина': (
                            f'{self.random_pene_credit()}'),
                        # 'Дата смерти': f'{person_list[41]}',
                        # остальные поля можно оставить пустыми или заполнить
                    }
                rows[0].update(rows_update)
            if override_contract and not have_security:
                number_contract = f'{person_list[44]}'
                have_security_ct = have_security_ct
                credit_id = credit_id
                rows_update = {
                        'Номер договора': f'{number_contract}',
                        'Кредиты # ID': f'{credit_id}',
                        'Сумма выдачи': f'{self.random_sum_credit()}',
                        'Валюта кредита': f'{person_list[17]}',
                        'Сумма аннуитета': f'{self.random_pene_credit()}',
                        'Просроченная ссудная задолженность, руб.': (
                            f'{self.random_pene_credit()}'),
                        'Неучтенные проценты за кредит, руб.': (
                            f'{self.random_pene_credit()}'),
                        'Неучтенные проценты (выкупленные), руб': (
                            f'{self.random_pene_credit()}'),
                        'Учтенные проценты за кредит, руб': (
                            f'{self.random_pene_credit()}'),
                        'Срочные проценты на внебалансе, руб.': (
                            f'{self.random_pene_credit()}'),
                        'Просроченная задолженность ' +
                        'по проц. на внебалансе, руб.': (
                            f'{self.random_pene_credit()}'),
                        'Просроченная задолженность по процентам, руб.': (
                            f'{self.random_pene_credit()}'),
                        'Просроченные проценты (выкупленные), руб': (
                            f'{self.random_pene_credit()}'),
                        'Общая задолженность, руб.': (
                            f'{self.random_pene_credit()}'),
                        'Признанные штрафы и пени': (
                            f'{self.random_pene_credit()}'),
                        'Присужденная госпошлина': (
                            f'{self.random_pene_credit()}'),
                        'Неприсужденная госпошлина': (
                            f'{self.random_pene_credit()}'),
                        # 'Дата смерти': f'{person_list[41]}',
                        # остальные поля можно оставить пустыми или заполнить
                    }
                rows[0].update(rows_update)
            if (
                override_person is True
                and guarantors is False
                and coborrowers is False
            ):
                number_contract = f'{person_list[44]}'
                credit_id = person_list[14]
                rows_update = {
                        'Номер договора': f'{number_contract}',
                        'Серия паспорта заемщика': (
                            f'{self.random_numeric_string(4)}'),
                        'Номер паспорта заемщика': (
                            f'{self.random_numeric_string(6)}'),
                        'Кредиты # ID': f'{credit_id}'
                        # остальные поля можно оставить пустыми или заполнить
                    }
                rows[0].update(rows_update)
            if (
                override_person is True
                and guarantors is True
                and coborrowers is True
            ):
                number_contract = f'{person_list[44]}'
                credit_id = person_list[14]
                rows_update = {
                        'Номер договора': f'{number_contract}',
                        'Серия паспорта заемщика': (
                            f'{self.random_numeric_string(4)}'),
                        'Номер паспорта заемщика': (
                            f'{self.random_numeric_string(6)}'),
                        'Кредиты # ID': f'{credit_id}',
                        'ФИО Созаемщика': f'{coborrower_list[0]}',
                        'Дата рождения Созаемщика': f'{coborrower_list[1]}',
                        'Место рождения созаемщика': f'{coborrower_list[2]}',
                        'Серия паспорта созаемщика': f'{
                            self.random_numeric_string(4)}',
                        'Номер паспорта созаемщика': f'{
                            self.random_numeric_string(6)}',
                        'Дата выдачи паспорта созаемщика': (
                            f'{coborrower_list[5]}'),
                        'Кем выдан Паспорт созаемщику': (
                            f'{coborrower_list[6]}'),
                        'Адрес регистрации созаемщика': (
                            f'{coborrower_list[7]}'),
                        'Место жительства созаемщика': f'{coborrower_list[8]}',
                        'Почтовый адрес созаемщика': f'{coborrower_list[9]}',
                        'Мобильный телефон созаемщика': (
                            f'{coborrower_list[10]}'),
                        'ФИО Поручителя': f'{guarantor_list[0]}',
                        'Дата рождения Поручителя': f'{guarantor_list[1]}',
                        'Место рождения Поручителя': f'{guarantor_list[2]}',
                        'Серия паспорта Поручителя': f'{guarantor_list[3]}',
                        'Номер паспорта Поручителя': f'{guarantor_list[4]}',
                        'Дата выдачи паспорта Поручителя': (
                            f'{guarantor_list[5]}'),
                        'Кем выдан Паспорт Поручителя': (
                            f'{guarantor_list[6]}'),
                        'Адрес регистрации Поручителя': f'{guarantor_list[7]}',
                        'Место жительства Поручителя': f'{guarantor_list[8]}',
                        'Почтовый адрес Поручителя': f'{guarantor_list[9]}',
                        'Телефон поручителя': f'{guarantor_list[10]}',
                        'Поручитель ЮЛ: Наименование': f'{guarantor_list[11]}',
                        'Поручитель ЮЛ: ИНН': f'{guarantor_list[12]}',
                        'Поручитель ЮЛ: Адрес регистрации': (
                            f'{guarantor_list[13]}'),
                        'Поручитель ЮЛ: Фактический Адрес': (
                            f'{guarantor_list[14]}')
                        # остальные поля можно оставить пустыми или заполнить
                    }
                rows[0].update(rows_update)
            if (
                override_contract is False
                and override_person is False
                and guarantors is False
                and coborrowers is False
            ):
                rows = rows
            if (
                override_contract is False
                and override_person is False
                and guarantors is True

            ):
                rows_update = {
                        'ФИО Поручителя': f'{guarantor_list[0]}',
                        'Дата рождения Поручителя': f'{guarantor_list[1]}',
                        'Место рождения Поручителя': f'{guarantor_list[2]}',
                        'Серия паспорта Поручителя': f'{guarantor_list[3]}',
                        'Номер паспорта Поручителя': f'{guarantor_list[4]}',
                        'Дата выдачи паспорта Поручителя': (
                            f'{guarantor_list[5]}'),
                        'Кем выдан Паспорт Поручителя': (
                            f'{guarantor_list[6]}'),
                        'Адрес регистрации Поручителя': f'{guarantor_list[7]}',
                        'Место жительства Поручителя': f'{guarantor_list[8]}',
                        'Почтовый адрес Поручителя': f'{guarantor_list[9]}',
                        'Телефон поручителя': f'{guarantor_list[10]}',
                        'Поручитель ЮЛ: Наименование': f'{guarantor_list[11]}',
                        'Поручитель ЮЛ: ИНН': f'{guarantor_list[12]}',
                        'Поручитель ЮЛ: Адрес регистрации': (
                            f'{guarantor_list[13]}'),
                        'Поручитель ЮЛ: Фактический Адрес': (
                            f'{guarantor_list[14]}')
                        # остальные поля можно оставить пустыми или заполнить
                    }
                rows[0].update(rows_update)
            if (
                override_contract is False
                and override_person is False
                and guarantors is True
                and override_guarantors is True
            ):
                number_contract = f'{guarantor_list[15]}'
                credit_id = guarantor_list[16]
                new_IO = guarantor_list[0].split()[1:]
                new_FIO = f'{self.choose_surname()} {
                    new_IO[0]} {new_IO[1]}'
                rows_update = {
                        'Номер договора': f'{number_contract}',
                        'Кредиты # ID': f'{credit_id}',
                        'ФИО Поручителя': f'{new_FIO}',
                        'Дата рождения Поручителя': f'{guarantor_list[1]}',
                        'Место рождения Поручителя': f'{guarantor_list[2]}',
                        'Серия паспорта Поручителя': f'{guarantor_list[3]}',
                        'Номер паспорта Поручителя': f'{guarantor_list[4]}',
                        'Дата выдачи паспорта Поручителя': (
                            f'{guarantor_list[5]}'),
                        'Кем выдан Паспорт Поручителя': (
                            f'{guarantor_list[6]}'),
                        'Адрес регистрации Поручителя': f'{guarantor_list[7]}',
                        'Место жительства Поручителя': f'{guarantor_list[8]}',
                        'Почтовый адрес Поручителя': f'{guarantor_list[9]}',
                        'Телефон поручителя': (
                            f'{self.random_numeric_string(10)}'),
                        'Поручитель ЮЛ: Наименование': f'{guarantor_list[11]}',
                        'Поручитель ЮЛ: ИНН': f'{guarantor_list[12]}',
                        'Поручитель ЮЛ: Адрес регистрации': (
                            f'{guarantor_list[13]}'),
                        'Поручитель ЮЛ: Фактический Адрес': (
                            f'{guarantor_list[14]}')
                        # остальные поля можно оставить пустыми или заполнить
                    }
                rows[0].update(rows_update)
            if (
                override_contract is False
                and override_person is False
                and coborrowers is True
            ):
                rows_update = {
                        'ФИО Созаемщика': f'{coborrower_list[0]}',
                        'Дата рождения Созаемщика': f'{coborrower_list[1]}',
                        'Место рождения созаемщика': f'{coborrower_list[2]}',
                        'Серия паспорта созаемщика': f'{coborrower_list[3]}',
                        'Номер паспорта созаемщика': f'{coborrower_list[4]}',
                        'Дата выдачи паспорта созаемщика': (
                            f'{coborrower_list[5]}'),
                        'Кем выдан Паспорт созаемщику': (
                            f'{coborrower_list[6]}'),
                        'Адрес регистрации созаемщика': (
                            f'{coborrower_list[7]}'),
                        'Место жительства созаемщика': f'{coborrower_list[8]}',
                        'Почтовый адрес созаемщика': f'{coborrower_list[9]}',
                        'Мобильный телефон созаемщика': (
                            f'{coborrower_list[10]}')
                        # остальные поля можно оставить пустыми или заполнить
                    }
                rows[0].update(rows_update)
            if (
                override_contract is False
                and override_person is False
                and coborrowers is True
                and override_coborrowers is True
            ):
                number_contract = f'{coborrower_list[11]}'
                credit_id = coborrower_list[12]
                new_IO = coborrower_list[0].split()[1:]
                new_FIO = f'{self.choose_surname()} {
                    new_IO[0]} {new_IO[1]}'
                rows_update = {
                        'Номер договора': f'{number_contract}',
                        'Кредиты # ID': f'{credit_id}',
                        'ФИО Созаемщика': f'{new_FIO}',
                        'Дата рождения Созаемщика': f'{coborrower_list[1]}',
                        'Место рождения созаемщика': f'{coborrower_list[2]}',
                        'Серия паспорта созаемщика': f'{coborrower_list[3]}',
                        'Номер паспорта созаемщика': f'{coborrower_list[4]}',
                        'Дата выдачи паспорта созаемщика': (
                            f'{coborrower_list[5]}'),
                        'Кем выдан Паспорт созаемщику': (
                            f'{coborrower_list[6]}'),
                        'Адрес регистрации созаемщика': (
                            f'{coborrower_list[7]}'),
                        'Место жительства созаемщика': f'{coborrower_list[8]}',
                        'Почтовый адрес созаемщика': f'{coborrower_list[9]}',
                        'Мобильный телефон созаемщика': (
                            f'{self.random_numeric_string(10)}')
                        # остальные поля можно оставить пустыми или заполнить
                    }
                rows[0].update(rows_update)
            with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(
                    f, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)
            return number_contract, credit_id
        except AssertionError:
            return pytest.fail(
                    'Произошла ошибка при генерации CSV файла импорта')
