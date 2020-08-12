from typing import Any

import requests
from django.core.management.base import BaseCommand

from core.models import Launch, Mission, Rocket, Site


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        print("Adding demo data...")
        launch_data = requests.get("https://api.spacexdata.com/v2/launches/").json()
        for data in launch_data:
            mission, _ = Mission.objects.get_or_create(
                name=data["mission_name"], defaults={"links": data["links"]}
            )
            site, _ = Site.objects.get_or_create(name=data["launch_site"]["site_name"])
            rocket, _ = Rocket.objects.get_or_create(
                name=data["rocket"]["rocket_name"],
                defaults={"rocket_type": data["rocket"]["rocket_type"]},
            )
            Launch.objects.create(mission=mission, site=site, rocket=rocket)
