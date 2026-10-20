import random
import string
import os
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate,
                                Paragraph,
                                Spacer,
                                Table,
                                TableStyle)
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def get_project_root():
    """Возвращает корневую директорию проекта"""
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent
    return project_root


def get_files_dir():
    """Возвращает директорию для хранения файлов в корне проекта"""
    project_root = get_project_root()
    files_dir = project_root / "pdf_files"
    files_dir.mkdir(exist_ok=True)
    return files_dir


def register_russian_font():
    """Регистрация шрифта с поддержкой кириллицы"""
    font_paths = [
        # Windows
        "C:/Windows/Fonts/arial.ttf",
        # Windows Calibri
        "C:/Windows/Fonts/calibri.ttf",
        # Linux
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        # MacOS
        "/System/Library/Fonts/Arial.ttf"
    ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('RussianFont', font_path))
                return 'RussianFont'
            except Exception:
                continue

    print(
        "⚠️ Шрифт с поддержкой кириллицы не найден, используется стандартный")
    return 'Helvetica'


def generate_pdf(typeDoc=None):
    """Генерация PDF с текущей датой и случайным заемщиком"""

    # Регистрируем шрифт для кириллицы
    russian_font = register_russian_font()

    # Получаем директорию для файлов в корне проекта
    files_dir = get_files_dir()

    # Данные
    current_date = datetime.now().strftime("%d.%m.%Y")
    random_borrower = ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=13))

    # Путь к файлу
    safe_date = current_date.replace('.', '_')
    if typeDoc == 1:
        filename = f"Расчет_задолженности_на_дату_{safe_date}.pdf"
    elif typeDoc == 2:
        filename = f"Квитанция_об_оплате_пошлины_{safe_date}.pdf"
    else:
        # Если тип не указан, генерируем с общим именем
        filename = f"Документ_{safe_date}.pdf"

    file_path = files_dir / filename  # Path object

    # Создание PDF
    doc = SimpleDocTemplate(str(file_path),  # преобразуем Path в строку
                            pagesize=A4,
                            leftMargin=15*mm, rightMargin=15*mm,
                            topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()

    # Стили с поддержкой кириллицы
    normal_style = ParagraphStyle(
        'Normal', parent=styles['Normal'],
        fontName=russian_font, fontSize=9, spaceAfter=8,
        encoding='utf-8'
    )

    title_style = ParagraphStyle(
        'Title', parent=styles['Heading1'],
        fontName=russian_font, fontSize=14, alignment=1, spaceAfter=20,
        encoding='utf-8'
    )

    story = [
        Paragraph("Распоряжение", title_style),
        Spacer(1, 10),
        Paragraph(f"Дата распоряжения: {current_date}", normal_style),
        Spacer(1, 10),
        Paragraph(
            "От кого: Отдел сопровождения работы с проблемными активами",
            normal_style),
        Paragraph(
            "Кому: Управление учета активно-пассивных операций",
            normal_style),
        Spacer(1, 10),
        Paragraph(
            "Прошу перенести всю сумму текущей задолженности по основному" +
            " долгу и процентам на просроченную с 31.03.2025 и приостановить" +
            " начисление штрафных санкций (пени) с 01.04.2025 в связи с " +
            "наступлением случая досрочного истребования и неисполнением " +
            "требования о досрочном возврате Кредита и истребовании Предмета" +
            " залога по Кредитному договору:", normal_style),
        Spacer(1, 10)
    ]

    table_data = [
        ['ЗАЁМЩИК', '№ КД', 'ДАТА КД', 'ВИД КД'],
        [random_borrower, '1231233.0/13050/2022-А', '14.08.2022',
         'Автокредит_2 документа (аннуитет)']
    ]

    table = Table(table_data, colWidths=[50*mm, 45*mm, 30*mm, 60*mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), russian_font),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTNAME', (0, 1), (-1, -1), russian_font),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('PADDING', (0, 0), (-1, -1), 3),
        ('WORDWRAP', (0, 0), (-1, -1), True),
    ]))

    story.extend([
        table,
        Spacer(1, 20),
        Paragraph(
            "Прошу сообщить окончательную сумму задолженности по Кредитному" +
            " договору по состоянию на 31.03.2025.", normal_style),
        Spacer(1, 10),
        Paragraph("- сумма основного долга;", normal_style),
        Paragraph("- сумма процентов за пользование кредитом;", normal_style),
        Paragraph("- сумма штрафов (пени).", normal_style),
        Spacer(1, 20),
        Paragraph(
            "Главный специалист отдела сопровождения работы с проблемными" +
            " активами Сметнева Е.Е.", normal_style),
        Spacer(1, 5),
        Paragraph(
            "Начальник отдела сопровождения работы с проблемными активами" +
            " Ягодкина Т.В.", normal_style)
    ])

    doc.build(story)

    # Проверяем создание файла
    if file_path.exists() and file_path.stat().st_size > 0:
        print(f"✅ Файл создан: {file_path}")
        return str(file_path)  # возвращаем строку для совместимости
    else:
        print("❌ Ошибка: файл не создан или пустой")
        return None
