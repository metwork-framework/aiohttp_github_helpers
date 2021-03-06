from aiohttp import ClientSession
import pytest  # noqa: F401
import pytest_asyncio.plugin  # noqa: F401

import aiohttp_github_helpers as h

TEST_OWNER = "metwork-framework"
TEST_REPO = "testrepo"


@pytest.mark.asyncio
async def test_github_get_labels_on_issue():
    async with ClientSession() as client_session:
        labels = await h.github_get_labels_on_issue(client_session, TEST_OWNER,
                                                    TEST_REPO, 38)
        assert len(labels) == 2
        assert sorted(labels)[0] == 'Priority: Low'
        assert sorted(labels)[1] == 'Status: Closed'


@pytest.mark.asyncio
async def test_github_get_pr_commit_messages_list():
    async with ClientSession() as client_session:
        messages = await h.github_get_pr_commit_messages_list(client_session,
                                                              TEST_OWNER,
                                                              TEST_REPO,
                                                              58)
        assert len(messages) == 1
        assert messages[0] == 'Update README.md'


@pytest.mark.asyncio
async def test_github_get_statuses():
    ref = "129ae457d5cd404ec76ab51ae70dbc137b4aae6d"
    async with ClientSession() as client_session:
        status = await h.github_get_status(client_session, TEST_OWNER,
                                           TEST_REPO, ref)
        assert status == 'failure'


@pytest.mark.asyncio
async def test_github_get_open_prs_by_sha():
    sha = "129ae457d5cd404ec76ab51ae70dbc137b4aae6d"
    async with ClientSession() as client_session:
        prs = await h.github_get_open_prs_by_sha(client_session, TEST_OWNER,
                                                 TEST_REPO, sha,
                                                 state='all')
        assert len(prs) == 1
        assert prs[0] == 61


@pytest.mark.asyncio
async def test_github_get_org_repos_by_topic():
    async with ClientSession() as client_session:
        repos = await h.github_get_org_repos_by_topic(client_session,
                                                      TEST_OWNER)
        assert len(repos) > 5
        repos = await h.github_get_org_repos_by_topic(client_session,
                                                      TEST_OWNER,
                                                      ["metwork"])
        assert len(repos) > 0
        repos = await h.github_get_org_repos_by_topic(client_session,
                                                      TEST_OWNER,
                                                      ["not_found"])
        assert len(repos) == 0
        repos = await h.github_get_org_repos_by_topic(client_session,
                                                      TEST_OWNER,
                                                      ["metwork"],
                                                      ["metwork"])
        assert len(repos) == 0


@pytest.mark.asyncio
async def test_github_get_latest_commit():
    async with ClientSession() as client_session:
        (sha, age) = await h.github_get_latest_commit(client_session,
                                                      TEST_OWNER, TEST_REPO,
                                                      "master")
        assert len(sha) == 40
        assert age > 1


@pytest.mark.asyncio
async def test_github_get_repo_topics():
    async with ClientSession() as client_session:
        topics = await h.github_get_repo_topics(client_session,
                                                TEST_OWNER, TEST_REPO)
        assert len(topics) > 1
        assert "testrepo" in topics


@pytest.mark.asyncio
async def test_github_get_pr_reviews():
    async with ClientSession() as client_session:
        reviews = await h.github_get_pr_reviews(client_session,
                                                TEST_OWNER, TEST_REPO, 81)
        assert len(reviews) == 1
        assert reviews[0]['sha'] == '04c830ffccc17bb90119cd3a89a151faba63ec97'
        assert reviews[0]['user_login'] == 'metworkbot'
        assert reviews[0]['state'] == 'APPROVED'
