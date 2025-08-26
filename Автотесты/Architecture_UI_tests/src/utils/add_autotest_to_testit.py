import testit_api_client
from testit_api_client.api import auto_tests_api
from testit_api_client.api import project_sections_api

from testit_api_client.api import work_items_api
from testit_api_client.api import sections_api
from testit_api_client.models.create_work_item_api_model import (
    CreateWorkItemApiModel,
)
from testit_api_client.models.step_post_model import StepPostModel
from testit_api_client.models.work_item_entity_types import WorkItemEntityTypes
from testit_api_client.models.work_item_priority_model import (
    WorkItemPriorityModel,
)
from testit_api_client.models.work_item_states import WorkItemStates
from testit_api_client.models.section_post_model import SectionPostModel
from src.utils.gherkin2testit_model import get_autotests_to_push_into_testit

from src.conf import settings


def cast_steps_to_workitem_model(step_types, steps):
    result = []
    when_index = -1

    for step_type, step in zip(step_types, steps):
        if step_type == "Action":
            when_index += 1
            result.append({"action": step["title"], "expected": ""})
        elif step_type == "Outcome":
            if when_index >= 0:
                result[when_index]["expected"] = (
                    f"{result[when_index]["expected"]}{step["title"]}\n"
                )
            else:
                raise ValueError(
                    "Найден 'Outcome', без предшествующего 'Action'"
                )

    return result


def create_autotest_and_work_items(
    autotest: dict,
    section_names: dict,
    api_autotest: auto_tests_api.AutoTestsApi,
    api_workitem: work_items_api.WorkItemsApi,
):
    api_response = api_autotest.create_auto_test(autotest)
    api_response = api_workitem.create_work_item(
        CreateWorkItemApiModel.from_dict(
            {
                "entityTypeName": WorkItemEntityTypes.TESTCASES.value,
                "state": WorkItemStates.READY.value,
                "priority": WorkItemPriorityModel.MEDIUM.value,
                "name": autotest.name,
                # TODO поправить это чудовище
                "steps": [
                    StepPostModel.from_dict(item).to_dict()
                    for item in cast_steps_to_workitem_model(
                        step_types, step_dict
                    )
                ],
                "preconditionSteps": [
                    {"action": step.title} for step in autotest.setup
                ],
                "postconditionSteps": [],
                "duration": 2,
                "projectId": settings.TEST_IT_PROJECT_ID,
                "attributes": {},
                "links": [],
                "tags": [],
                "sectionId": section_names[autotest.classname]["id"],
                "autoTests": [{"id": api_response.model_dump()["id"]}],
                "sourceType": "Manual",
            }
        )
    )


def get_workitems_section_names(
    api_project_section: project_sections_api.ProjectSectionsApi,
):
    section_names = {
        item.name: {"id": item.id, "parent_id": item.id}
        for item in api_project_section.get_sections_by_project_id(
            project_id=settings.TEST_IT_PROJECT_ID
        )
    }
    return section_names


def create_workitems_sections(
    section_names: dict, api_section: sections_api.SectionsApi
):
    if autotest.namespace not in section_names:
        api_response = api_section.create_section(
            SectionPostModel.from_dict(
                {
                    "projectId": settings.TEST_IT_PROJECT_ID,
                    "parentId": settings.TEST_IT_MAIN_SECTION_ID,
                    "name": autotest.namespace,
                    "attachments": [],
                }
            )
        )
        namespace_id = api_response.model_dump()["id"]
        section_names.update(
            {
                autotest.namespace: {
                    "id": namespace_id,
                    "parent_id": settings.TEST_IT_MAIN_SECTION_ID,
                }
            }
        )

    if autotest.classname not in section_names:
        api_response = api_section.create_section(
            SectionPostModel.from_dict(
                {
                    "projectId": settings.TEST_IT_PROJECT_ID,
                    "parentId": section_names[autotest.namespace]["id"],
                    "name": autotest.classname,
                    "attachments": [],
                }
            )
        )
        classname_id = api_response.model_dump()["id"]
        section_names.update(
            {
                autotest.classname: {
                    "id": classname_id,
                    "parent_id": settings.TEST_IT_PROJECT_ID,
                }
            }
        )


if __name__ == "__main__":
    with testit_api_client.ApiClient(settings.configuration) as api_client:
        api_autotest = auto_tests_api.AutoTestsApi(api_client)
        api_workitem = work_items_api.WorkItemsApi(api_client)
        api_section = sections_api.SectionsApi(api_client)
        api_project_section = project_sections_api.ProjectSectionsApi(
            api_client
        )
        sections = get_workitems_section_names(api_project_section)
        for autotest in get_autotests_to_push_into_testit():
            try:
                autotest, step_types = autotest
                step_dict = [step.to_dict() for step in autotest.steps]
                create_workitems_sections(sections, api_section)

                create_autotest_and_work_items(
                    autotest, sections, api_autotest, api_workitem
                )
            except Exception as e:
                print(e)
