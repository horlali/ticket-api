import jira
import pytest
import requests
import requests_mock

from src.services.jira import JiraSvc


@pytest.fixture
def adapter():
    return requests_mock.Adapter()


@pytest.fixture
def svc(adapter):
    svc = JiraSvc(
        url="https://jira.atlassian.com",
        user="test",
        token="xxx",
        get_server_info=False,
    )
    session = requests.Session()
    session.mount("https://", adapter)
    svc._session = session
    return svc


class TestJiraSvc:
    def test_content(self, svc, adapter):
        path = svc._get_url("test")
        adapter.register_uri("GET", path, text="data")
        assert svc.content("test") == b"data"

    def test_exists_issue(self, svc, mocker):
        mocker.patch.object(svc, "issue", return_value="")
        assert svc.exists_issue("Jira-123") is True

        mocker.patch.object(svc, "issue", side_effect=jira.JIRAError(status_code=404))
        assert svc.exists_issue("Jira-123") is False

    def test_has_permissions(self, svc, adapter):
        path = svc._get_url("mypermissions")
        data = {"permissions": {}}
        adapter.register_uri("GET", path, json=data)
        assert svc.has_permissions(permissions=[]) is True
        assert svc.has_permissions(permissions=["perm"]) is False
        data["permissions"]["perm1"] = {"havePermission": True}
        adapter.register_uri("GET", path, json=data)
        assert svc.has_permissions(permissions=["perm1"]) is True
        assert svc.has_permissions(permissions=["perm1", "perm2"]) is False
        data["permissions"]["perm2"] = {"havePermission": False}
        adapter.register_uri("GET", path, json=data)
        assert svc.has_permissions(permissions=["perm1"]) is True
        assert svc.has_permissions(permissions=["perm2"]) is False
        assert svc.has_permissions(permissions=["perm1", "perm2"]) is False
