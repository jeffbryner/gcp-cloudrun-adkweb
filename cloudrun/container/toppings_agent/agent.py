from google.adk.agents import Agent
import os
import google.auth

credentials, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"  # change to suitable location

root_agent = Agent(
    model="gemini-2.5-flash",
    name="toppings_agent",
    instruction="You are an expert in ice cream toppings. When asked you can always recommend a topping.",
)
