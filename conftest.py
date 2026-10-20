import allure
import pytest
import shutil
from pathlib import Path
from playwright.sync_api import Page


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        "viewport": {
            "width": 1920,
            "height": 1080,
        }
    }


@pytest.fixture(scope="function", autouse=True)
def add_artifacts_on_failure(page: Page, request):
    """Фикстура для автоматического прикрепления артефактов
    к Allure-отчету при падении теста."""
    yield
    # Проверяем, завершился ли тест с ошибкой
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:

        # 1. Прикрепляем скриншот
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name="screenshot",
            attachment_type=allure.attachment_type.PNG
        )

        # 2. Прикрепляем HTML-код страницы на момент падения
        html_content = page.content()
        allure.attach(
            html_content,
            name="page_content",
            attachment_type=allure.attachment_type.HTML
        )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для захвата результата выполнения теста и передачи его в фикстуру.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session", autouse=True)
def clean_allure_dirs():
    """Очищает папки allure-results и allure-report перед началом тестов"""
    # Очищаем папку с результатами тестов
    results_dir = Path("allure-results")
    if results_dir.exists():
        shutil.rmtree(results_dir)
    results_dir.mkdir(exist_ok=True)
    # Очищаем папку с финальным отчётом
    report_dir = Path("allure-report")
    if report_dir.exists():
        shutil.rmtree(report_dir)
