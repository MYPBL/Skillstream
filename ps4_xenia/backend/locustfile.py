from locust import HttpUser, task, between
import random

class PlatformUser(HttpUser):
    wait_time = between(1, 3) # Wait 1-3 seconds between tasks
    token = None
    user_id = None

    def on_start(self):
        """Login on start"""
        # Alternate between Admin and Newbie to mix cache keys
        email = "admin@example.com" if random.random() > 0.5 else "newbie@example.com"
        password = "password123"
        
        with self.client.post("/api/v1/auth/login", json={"email": email, "password": password}) as res:
            if res.status_code == 200:
                self.token = res.json()["access_token"]
                # Get User ID
                headers = {"Authorization": f"Bearer {self.token}"}
                me = self.client.get("/api/v1/auth/me", headers=headers).json()
                self.user_id = me["id"]
            else:
                print(f"Login failed for {email}")

    @task(3)
    def view_dashboard(self):
        """Heavy Dashboard Load"""
        if self.token and self.user_id:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get(f"/api/v1/learning/dashboard/{self.user_id}", headers=headers)

    @task(5)
    def view_analytics_overview(self):
        """Should be cached"""
        if self.token and self.user_id:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get(f"/api/v1/analytics/{self.user_id}/overview", headers=headers)

    @task(2)
    def view_recommendations(self):
        """Complex Query"""
        if self.token and self.user_id:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get(f"/api/v1/learning/{self.user_id}/recommendations", headers=headers)

    @task(1)
    def health_check(self):
        self.client.get("/health")
