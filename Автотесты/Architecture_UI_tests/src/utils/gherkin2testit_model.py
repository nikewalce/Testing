import re
from gherkin.parser import Parser
from pathlib import Path
from testit_api_client.models.auto_test_post_model import AutoTestPostModel
from testit_api_client.models.auto_test_step_model import AutoTestStepModel
from src.conf import settings


def get_raw_feature_data(path: str):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return content


def parse_feature_file(data: str):
    parser = Parser()
    return parser.parse(data)


def extract_examples(scenario):
    all_examples = []
    for example in scenario.get("examples", []):
        headers = [cell["value"] for cell in example["tableHeader"]["cells"]]
        for row in example["tableBody"]:
            values = [cell["value"] for cell in row["cells"]]
            example_dict = dict(zip(headers, values))
            all_examples.append(example_dict)
    return all_examples


def replace_all_keywords(text: str, values: dict) -> str:
    return re.sub(r"<([^>]+)>", lambda m: values.get(m.group(1), m.group(0)), text)


def parse_tags(scenario: dict, replace_dict: dict = {}) -> dict:
    result_dict = {}
    for tag in scenario["tags"]:
        if tag["name"] == "@skip":
            continue
        tag_name, tag_value = tag["name"].split("=")
        tag_value = replace_all_keywords(tag_value, replace_dict)
        if "@ExternalId" in tag_name:
            result_dict["externalId"] = tag_value
        if "@NameSpace" in tag_name:
            result_dict["namespace"] = tag_value
        if "@ClassName" in tag_name:
            result_dict["classname"] = tag_value
    return result_dict


def parse_steps(scenario: dict, replace_dict: dict = {}) -> dict:
    result_dict = {}
    step_types = []
    if steps := scenario.get("steps"):
        steps_to_add_setup = []
        steps_to_add_main = []
        current_step_type = steps[0]["keywordType"]
        for step in steps:
            if not step["keywordType"] == "Unknown":
                current_step_type = step["keywordType"]

            text = step["text"]
            text = replace_all_keywords(text, replace_dict)

            if current_step_type != "Context":
                steps_to_add_main.append(AutoTestStepModel(title=text))
                step_types.append(current_step_type)
            else:
                steps_to_add_setup.append(AutoTestStepModel(title=text))
        result_dict["setup"] = steps_to_add_setup
        result_dict["steps"] = steps_to_add_main
    return result_dict, step_types


def get_autotests_to_push_into_testit():
    to_create = []
    pathlist = Path("tests/features/").rglob("*.feature")
    for path in pathlist:
        filepath = str(path)
        raw_data = get_raw_feature_data(filepath)
        data: dict = parse_feature_file(raw_data)

        background = data["feature"]["children"][0].get("background")

        for child in data["feature"]["children"]:
            step_types = []
            result_dict = {
                "projectId": settings.TEST_IT_PROJECT_ID,
            }

            if not (scenario := child.get("scenario")):
                continue

            if background:
                scenario_steps = background["steps"][:]
                scenario_steps.extend(scenario["steps"])
                scenario["steps"] = scenario_steps[:]

            if replaces := extract_examples(scenario):
                for num, replace_dict in enumerate(replaces, 1):
                    try:
                        result_dict.update(parse_tags(scenario, replace_dict))
                        steps, step_types = parse_steps(scenario, replace_dict)
                        result_dict.update(steps)
                    except Exception as e:
                        print(f"{filepath} -> {e}")

                    result_dict["name"] = replace_all_keywords(
                        scenario["name"], replace_dict
                    )

                    result_dict["externalId"] += f"_{num}"

                    to_create.append((AutoTestPostModel(**result_dict), step_types))
            else:
                try:
                    result_dict.update(parse_tags(scenario))
                    steps, step_types = parse_steps(scenario)
                    result_dict.update(steps)
                except Exception as e:
                    print(f"{filepath} -> {e}")
                result_dict["name"] = scenario["name"]
                to_create.append((AutoTestPostModel(**result_dict), step_types))

    return to_create


if __name__ == "__main__":
    get_autotests_to_push_into_testit()
