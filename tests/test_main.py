import unittest

import httpx

from main import app


class ApiSmokeTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        transport = httpx.ASGITransport(app=app)
        self.client = httpx.AsyncClient(transport=transport, base_url="http://test")

    async def asyncTearDown(self):
        await self.client.aclose()

    async def test_root_reports_catalog_counts(self):
        response = await self.client.get("/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["name"], "Dart Portal API")
        self.assertGreaterEqual(payload["counts"]["pros"], 3)
        self.assertGreaterEqual(payload["counts"]["events"], 1)

    async def test_health_endpoint(self):
        response = await self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    async def test_pros_are_sorted_by_popularity(self):
        response = await self.client.get("/pros?sort=popularity&limit=2")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 2)
        self.assertGreaterEqual(payload[0]["popularity_score"], payload[1]["popularity_score"])

    async def test_events_filter_by_area(self):
        response = await self.client.get("/events?area=Hyogo")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload)
        self.assertTrue(all(item["area"] == "Hyogo" for item in payload))

    async def test_recommendations_return_gear_bundles(self):
        response = await self.client.post(
            "/recommendations",
            json={"area": "Hyogo", "favorite_pro_ids": [101], "budget": 20000},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["events"])
        self.assertTrue(payload["gear_bundles"])
        self.assertGreater(payload["score"], 0)

    async def test_offers_return_matching_event(self):
        response = await self.client.post(
            "/offers",
            json={"area": "Hyogo", "favorite_pro_ids": [101], "budget": 20000},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload)
        self.assertEqual(payload[0]["event"]["area"], "Hyogo")


if __name__ == "__main__":
    unittest.main()
