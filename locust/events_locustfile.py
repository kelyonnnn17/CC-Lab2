import uuid

from locust import HttpUser, between, task


class EventsUser(HttpUser):
    """
    Load test for the `/events` page.

    Notes:
    - Uses `params` instead of building a URL string (safer encoding).
    - Uses a stable `name` so Locust groups stats under `/events` (not per querystring).
    - Performs basic response validation so failures are visible in Locust.
    """

    wait_time = between(1, 2)

    def on_start(self) -> None:
        # Unique-ish per simulated user to better reflect real traffic.
        self.username = f"locust_{uuid.uuid4().hex[:8]}"

    @task
    def view_events(self) -> None:
        with self.client.get(
            "/events",
            params={"user": self.username},
            name="/events",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"HTTP {resp.status_code}")
                return

            # Lightweight sanity check that we got the expected page.
            if "🎪 Events" not in resp.text:
                resp.failure("Unexpected response body (missing Events marker)")
