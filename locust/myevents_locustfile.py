import uuid

from locust import HttpUser, between, task


class MyEventsUser(HttpUser):
    """
    Load test for the `/my-events` page.

    Improvements:
    - Uses `params` instead of building a URL string.
    - Uses a stable `name` so Locust aggregates stats under `/my-events`.
    - Performs basic response validation so server errors show as failures.
    """

    wait_time = between(1, 2)

    def on_start(self) -> None:
        self.username = f"locust_{uuid.uuid4().hex[:8]}"

    @task
    def view_my_events(self) -> None:
        with self.client.get(
            "/my-events",
            params={"user": self.username},
            name="/my-events",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"HTTP {resp.status_code}")
                return

            # Page always includes this header even when no events are registered.
            if "✅ My Events" not in resp.text:
                resp.failure("Unexpected response body (missing My Events marker)")
