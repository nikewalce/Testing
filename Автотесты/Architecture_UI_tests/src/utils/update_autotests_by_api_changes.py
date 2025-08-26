import re
import testit_api_client

from testit_api_client.api import work_items_api
from testit_api_client.models.work_item_select_api_model import (
    WorkItemSelectApiModel,
)
from testit_api_client.models.work_item_filter_api_model import (
    WorkItemFilterApiModel,
)
from testit_api_client.models.work_item_put_model import WorkItemPutModel


from src.support.logging.logger import Logger
from src.conf import settings
from decouple import config
import json


def data_str_to_regex_pattern(data_str: str) -> str:
    escaped_data_str = re.sub(r"([.^$+*?[\]\\\\|()])", r"\\\1", data_str)
    pattern = re.sub(r"\{[^}]+\}", r"[^/]+", escaped_data_str)

    return pattern


if __name__ == "__main__":
    logger = Logger("Изменения API")
    service_changes = json.loads(config("JSON_DATA"))

    with testit_api_client.ApiClient(settings.configuration) as api_client:
        api_workitem = work_items_api.WorkItemsApi(api_client)

        workitems = api_workitem.api_v2_work_items_search_post(
            work_item_select_api_model=WorkItemSelectApiModel(
                filter=WorkItemFilterApiModel(
                    isDeleted=False,
                    isAutomated=True,
                    projectIds=[settings.TEST_IT_PROJECT_ID],
                )
            )
        )

        filtered_case_ids = [
            workitem.model_dump()["id"] for workitem in workitems
        ]

        updated = set()
        for case_id in filtered_case_ids:
            test_case = api_workitem.get_work_item_by_id(case_id)
            test_case_model = test_case.model_dump()
            for step in test_case_model.get("steps"):
                for service, items in service_changes.items():
                    if not items:
                        continue
                    for item in items:
                        http_method = item["type"]
                        url = item["url"].removeprefix("/public/")

                        test_case_model["sectionId"] = test_case_model[
                            "section_id"
                        ]
                        test_case_model["preconditionSteps"] = test_case_model[
                            "precondition_steps"
                        ]
                        test_case_model["postconditionSteps"] = (
                            test_case_model["postcondition_steps"]
                        )
                        data_str = f'"{http_method}" на "/{service}/{url}"'
                        pattern = data_str_to_regex_pattern(data_str)
                        if re.search(pattern, step.get("action")):
                            test_case_model["state"] = "NeedsWork"
                            item = WorkItemPutModel.from_dict(test_case_model)
                            api_workitem.update_work_item(item)
                            updated.add(case_id)
        logger.critical(f"Кейсов требующих доработки: {len(updated)}")
