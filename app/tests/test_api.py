from fastapi import status
import uuid, random


class TestIngredientsAPI:
    """Test cases for the ingredients API."""

    async def test_create_category(self, client, category_name="CategoryName"):
        response = await client.post("/categories/", json={"name": f"{category_name}"})
        assert response.status_code == status.HTTP_201_CREATED
        id = response.json().get("id")
        assert id is not None

        response = await client.get("/categories/")
        assert response.status_code == status.HTTP_200_OK
        # assert len(response.json()) == 1
        assert response.json()[0]["id"] == id

    async def test_create_parameter(
        self, client, parameter_name="Parameter", description="Description"
    ):
        response = await client.post(
            "/parameters/",
            json={
                "name": f"{parameter_name}",
                "description": f"{description}",
                "datatype": "str",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        id = response.json().get("id")
        assert id is not None

        response = await client.get("/parameters/")
        assert response.status_code == status.HTTP_200_OK
        # assert len(response.json()) == 1
        assert response.json()[0]["id"] == id

    async def test_create_dataset(self, client):
        for _ in range(100):
            await self.test_create_category(client, uuid.uuid4())
        for _ in range(100):
            await self.test_create_parameter(client, uuid.uuid4(), uuid.uuid4())
        for _ in range(100):
            dataset = uuid.uuid4()
            description = uuid.uuid4()
            category_id = random.randint(1, 99)
            pairs = []
            for _ in range(25):
                pairs.append(
                    {
                        "parameter_value": f"{uuid.uuid4()}",
                        "parameter_id": f"{random.randint(1, 99)}",
                    }
                )
            response = await client.post(
                "/datasets/",
                json={
                    "name": f"{dataset}",
                    "description": f"{description}",
                    "category_id": category_id,
                    "pairs": pairs,
                },
            )
        assert response.status_code == status.HTTP_201_CREATED
        id = response.json().get("id")
        assert id is not None

        response = await client.get("/datasets/")
        assert response.status_code == status.HTTP_200_OK
        # assert len(response.json()) == 1
        assert response.json()[0]["id"] == id
