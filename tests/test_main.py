import unittest

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class ApiSmokeTests(unittest.TestCase):
    def test_root_reports_catalog_counts(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["name"], "Dart Portal API")
        self.assertGreaterEqual(payload["counts"]["pros"], 3)
        self.assertGreaterEqual(payload["counts"]["events"], 1)

    def test_health_endpoint(self):
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_pros_are_sorted_by_popularity(self):
        response = client.get("/pros?sort=popularity&limit=2")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 2)
        self.assertGreaterEqual(payload[0]["popularity_score"], payload[1]["popularity_score"])

    def test_events_filter_by_area(self):
        response = client.get("/events?area=Hyogo")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload)
        self.assertTrue(all(item["area"] == "Hyogo" for item in payload))

    def test_recommendations_return_gear_bundles(self):
        response = client.post(
            "/recommendations",
            json={"area": "Hyogo", "favorite_pro_ids": [101], "budget": 20000},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["events"])
        self.assertTrue(payload["gear_bundles"])
        self.assertGreater(payload["score"], 0)

    def test_offers_return_matching_event(self):
        response = client.post(
            "/offers",
            json={"area": "Hyogo", "favorite_pro_ids": [101], "budget": 20000},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload)
        self.assertEqual(payload[0]["event"]["area"], "Hyogo")


if __name__ == "__main__":
    unittest.main()
