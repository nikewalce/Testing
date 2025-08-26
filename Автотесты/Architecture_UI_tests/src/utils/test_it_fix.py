# from os import fdopen, remove
# from shutil import copymode, move
# from tempfile import mkstemp
#
# from testit_api_client.models import test_run_v2_api_result
#
#
# def replace(file_path: str, pattern: str, subst: str) -> None:
#     """
#     Заменяет строку кода в модуле.
#
#     :file_path: Путь до модуля.
#     :param pattern: Строка, которую надо заменить.
#     :param subst: Строка, на которую заменяем."""
#
#     fh, abs_path = mkstemp()
#     with fdopen(fh, "w") as new_file:
#         with open(file_path) as old_file:
#             for line in old_file:
#                 new_file.write(line.replace(pattern, subst))
#     copymode(file_path, abs_path)
#     remove(file_path)
#     move(abs_path, file_path)
#
#
# if __name__ == "__main__":
#     path = test_run_v2_api_result.__file__
#     to_change = r"""    status: TestStatusApiResult = Field(description="Test run status")"""
#     replace(path, to_change, "")
#     to_change = r"""            "status": TestStatusApiResult.from_dict(obj["status"]) if obj.get("status") is not None else None,"""
#     replace(path, to_change, "")
#     to_change = r"""    __properties: ClassVar[List[str]] = ["id", "name", "description", "launchSource", "startedOn", "completedOn", "stateName", "status", "projectId", "testPlanId", "testResults", "createdDate", "modifiedDate", "createdById", "modifiedById", "createdByUserName", "attachments", "links", "customParameters", "webhooks", "runCount"]"""
#     changed = r"""    __properties: ClassVar[List[str]] = ["id", "name", "description", "launchSource", "startedOn", "completedOn", "stateName", "projectId", "testPlanId", "testResults", "createdDate", "modifiedDate", "createdById", "modifiedById", "createdByUserName", "attachments", "links", "customParameters", "webhooks", "runCount"]"""
#     replace(path, to_change, changed)
