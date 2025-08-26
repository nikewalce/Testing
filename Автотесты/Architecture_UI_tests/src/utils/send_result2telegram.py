import requests
from telebot import TeleBot
from collections import defaultdict

from src.conf import settings

bot = TeleBot(settings.TELEGRAM_TELEBOT_TOKEN, "HTML")
connected_chat = settings.TELEGRAM_CONNECTED_CHAT
api_token = settings.TEST_IT_TOKEN

headers = {
    "Content-Type": "application/json",
    "Authorization": f"PrivateToken {api_token}",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36 Edg/135.0.0.0",
}
domain = settings.TEST_IT_URL


def request_test_run(testrun_id):
    with requests.Session() as sess:
        response = sess.get(
            f"{domain}/api/v2/testRuns/{testrun_id}", headers=headers
        )
        resp = response.json()
    return resp


def send_testrun_result(testrun_id):
    try:
        testrun = request_test_run(testrun_id)
        if any(["error", "400", "401", "403", "500"]) in testrun:
            raise Exception(
                "Ошибка - проверьте авторизацию. Также проверьте, обращаетесь ли к корректному адресу, и правильно ли настроен вебхук TestIT."
            )
    except Exception as e:
        bot.send_message(connected_chat)
    try:
        testcount = len(testrun["testResults"])
        testcount_all_outcomes = [
            autotest["outcome"] for autotest in testrun["testResults"]
        ]
        testcount_failed = testcount_all_outcomes.count("Failed")
        testcount_passed = testcount_all_outcomes.count("Passed")
        testcount_skipped = testcount_all_outcomes.count("Skipped")
        testrun_name = testrun["name"]
        testrun_description = testrun["description"]
        launchSource = testrun["launchSource"]
        autotest_results = [
            {
                "test_name": autotest["autoTest"]["name"],
                "group": autotest["autoTest"]["classname"],
                "outcome": autotest["outcome"]
                .replace("Passed", "✅")
                .replace("Skipped", "⏩")
                .replace("Failed", "❌")
                + "\n",
            }
            for autotest in testrun["testResults"]
        ]
        groups = {}
        for autotest in autotest_results:
            groups.update({autotest["group"]: {"passed": 0, "failed": 0}})

        results = defaultdict(lambda: {"Passed": 0, "Failed": 0, "Skipped": 0})

        for autotest in testrun["testResults"]:
            # classname = autotest["autoTest"].get("classname")
            namespace = autotest["autoTest"].get("namespace")
            outcome = autotest.get("outcome")
            if (
                namespace and outcome in results[namespace]
            ):  # по необходимости поменять на classname (подгруппы)
                results[namespace][outcome] += 1

        report = (
            f"<b>Прогон завершён!\nИмя прогона: </b>{testrun_name}\n<b>Описание тестов: </b>{testrun_description}"
            f"\n<b>Кол-во тестов: </b>{testcount}\n<b>Прошло: </b>{testcount_passed}\n<b>Упало: </b>{testcount_failed}\n<b>Пропущено: </b>{testcount_skipped}"
            f"\n<b>Источник запуска тестов: </b>{launchSource}\n<b>Полный отчет в TestIT: </b>https://test-it/projects/1/test-runs/{testrun_id}\n\n"
        )
        by_group = "".join(
            [
                f"<b>{group}:</b>\n<b>Пройдено ✅:</b> {results[group].get("Passed")}\n<b>Упало ❌</b>: {results[group].get("Failed")}\n<b>Пропущено ⏩</b>: {results[group].get("Skipped")}\n\n"
                for group in dict(results)
            ]
        )
        report = report + by_group

    except KeyError as e:
        bot.send_message(
            connected_chat, f"Произошла ошибка! Не найден ключ: {e}"
        )
        raise KeyError(e)
    bot.send_message(connected_chat, report, parse_mode="HTML")
