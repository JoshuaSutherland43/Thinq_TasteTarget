from datetime import datetime
from typing import Dict, List
from backend.services.report_generator import ReportGenerator

import json


class ReportGenerator:

    def __init__(self, data):
        self.data = data

    @staticmethod
    def generate_report(data: Dict) -> str:
        report = f"""TASTETARGET INTELLIGENCE REPORT
    {'-' * 50}
    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    Product: {data['product_name']}

    AUDIENCE SEGMENTS
    {'-' * 50}"""

        for i, persona in enumerate(data["personas"], 1):
            report += f"""

    {i}. {persona['name'].upper()}
    {persona['description']}

    Psychographics:
    {chr(10).join(f'• {trait}' for trait in persona['psychographics'])}

    Channels:
    {chr(10).join(f'• {channel}' for channel in persona['preferred_channels'])}
    """

        report += f"""

    MESSAGING STRATEGY
    {'-' * 50}"""

        for copy in data["campaign_copies"]:
            persona_name = next(
                (
                    p["name"]
                    for p in data["personas"]
                    if p["persona_id"] == copy["persona_id"]
                ),
                "Unknown",
            )
            report += f"""

    {persona_name.upper()}:
    Tagline: {copy['tagline']}
    Social: {copy['social_caption']}
    Email: {copy['email_subject']}
    """

        return report

    @staticmethod
    def generate_json(data: dict) -> str:
        return json.dumps(data, indent=2)
