from httpx import AsyncClient


async def test_list_equipment(async_client: AsyncClient) -> None:
    response = await async_client.get("/equipment")

    assert response.status_code == 200
    equipment = response.json()
    assert len(equipment) == 12
    assert any(item["e_name"] == "A100 Compute Node" for item in equipment)


async def test_equipment_detail(async_client: AsyncClient) -> None:
    response = await async_client.get("/equipment/1")

    assert response.status_code == 200
    equipment = response.json()
    assert equipment["e_name"] == "A100 Compute Node"
    assert equipment["device_count"] == 2
    assert equipment["active_device_count"] == 2
    assert equipment["usage_count"] == 3


async def test_active_equipment_users(async_client: AsyncClient) -> None:
    response = await async_client.get("/equipment/1/active-users")

    assert response.status_code == 200
    users = response.json()
    assert users
    assert any(user["member_name"] == "Maya Chen" for user in users)
    assert all("projects" in user for user in users)


async def test_list_devices(async_client: AsyncClient) -> None:
    response = await async_client.get("/devices")

    assert response.status_code == 200
    devices = response.json()
    assert len(devices) == 20
    first = devices[0]
    assert "did" in first
    assert "eid" in first
    assert "status" in first


async def test_device_detail(async_client: AsyncClient) -> None:
    response = await async_client.get("/devices/1")

    assert response.status_code == 200
    device = response.json()
    assert device["equipment_name"] == "A100 Compute Node"
    assert device["equipment_type"] == "GPU Server"
    assert isinstance(device["active_user_count"], int)


async def test_active_usages(async_client: AsyncClient) -> None:
    response = await async_client.get("/uses?active_only=true")

    assert response.status_code == 200
    usages = response.json()
    assert usages
    assert all(usage["e_date"] is None for usage in usages)


async def test_create_usage_flow_and_delete_with_auth(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    equipment_response = await async_client.post(
        "/equipment",
        headers=auth_headers,
        json={
            "e_type": "Route Test Type",
            "e_name": "Route Test Equipment",
            "manual": "https://example.com/manuals/route-test",
        },
    )
    assert equipment_response.status_code == 201
    eid = equipment_response.json()["eid"]

    device_response = await async_client.post(
        "/devices",
        headers=auth_headers,
        json={"eid": eid, "status": "active", "p_date": "2026-04-27"},
    )
    assert device_response.status_code == 201
    did = device_response.json()["did"]

    usage_response = await async_client.post(
        "/uses",
        headers=auth_headers,
        json={
            "mid": 1,
            "did": did,
            "eid": eid,
            "s_date": "2026-04-27",
            "purpose": "Route test usage",
        },
    )
    assert usage_response.status_code == 201

    blocked_update = await async_client.put(
        f"/devices/{did}",
        headers=auth_headers,
        json={"eid": 1},
    )
    assert blocked_update.status_code == 400
    assert "device equipment cannot be changed" in blocked_update.json()["detail"]

    delete_usage = await async_client.delete(
        f"/uses/1/{did}/{eid}",
        headers=auth_headers,
    )
    assert delete_usage.status_code == 200
    assert delete_usage.json()["message"] == "usage deleted"

    delete_device = await async_client.delete(
        f"/devices/{did}",
        headers=auth_headers,
    )
    assert delete_device.status_code == 200
    assert delete_device.json()["message"] == "device deleted"

    delete_equipment = await async_client.delete(
        f"/equipment/{eid}",
        headers=auth_headers,
    )
    assert delete_equipment.status_code == 200
    assert delete_equipment.json()["message"] == "equipment deleted"


async def test_delete_seeded_equipment_blocked(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    response = await async_client.delete("/equipment/1", headers=auth_headers)

    assert response.status_code == 400
    assert "dependent records exist" in response.json()["detail"]
