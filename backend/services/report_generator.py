from datetime import datetime
from typing import Dict, List, Any
import json  # Keeping this import, though not directly used in the report generation string itself


class ReportGenerator:
    """
    Generates a comprehensive marketing intelligence report based on audience personas
    and campaign copies.
    """

    def __init__(self, data: Dict):
        """
        Initializes the ReportGenerator with the data.
        While __init__ is present, the generate_report method is static,
        so `self.data` isn't directly used by the static method.
        It's good practice to align if you intend to make it an instance method later.
        """
        self.data = data

    @staticmethod
    def generate_report(data: Dict) -> str:
        """
        Generates a detailed intelligence report.

        Args:
            data (Dict): A dictionary containing 'product_name', 'personas',
                         and 'campaign_copies'.

        Returns:
            str: The formatted intelligence report, or an error message if data is invalid.
        """
        if not data or not isinstance(data, dict):
            return "Error: No data provided or data is not a dictionary."

        required_keys = ["product_name", "personas", "campaign_copies"]

        # This print is still useful for debugging during development
        print(f"Data keys received by ReportGenerator: {list(data.keys())}")

        for key in required_keys:
            if key not in data:
                return f"Error: Missing required key '{key}' in provided data."
            # Also ensure lists are not empty if they are required to have content
            if key in ["personas", "campaign_copies"] and not data[key]:
                return f"Error: '{key}' cannot be empty."

        report_lines: List[str] = []
        product_name = data.get("product_name", "Unknown Product").upper()
        generated_date = datetime.now().strftime("%Y-%m-%d %H:%M")

        # --- Report Header ---
        report_lines.append("TASTETARGET INTELLIGENCE REPORT")
        report_lines.append("-" * 50)
        report_lines.append(f"Generated: {generated_date}")
        report_lines.append(f"Product: {product_name}")
        report_lines.append("")  # Add an empty line for spacing

        # --- Executive Summary (Placeholder - could be generated by LLM) ---
        report_lines.append("EXECUTIVE SUMMARY")
        report_lines.append("-" * 50)
        report_lines.append(
            f"This report provides a data-driven overview of the target audience segments "
            f"and tailored messaging strategies for **{product_name}**. "
            f"It identifies {len(data['personas'])} distinct audience personas and "
            f"provides {len(data['campaign_copies'])} personalized campaign messages."
        )
        report_lines.append("")

        # --- Audience Segments Section ---
        report_lines.append("AUDIENCE SEGMENTS")
        report_lines.append("-" * 50)
        report_lines.extend(
            ReportGenerator._generate_audience_segments(data["personas"])
        )
        report_lines.append("")

        # --- Messaging Strategy Section ---
        report_lines.append("MESSAGING STRATEGY")
        report_lines.append("-" * 50)
        report_lines.extend(
            ReportGenerator._generate_messaging_strategy(
                data["campaign_copies"], data["personas"]
            )
        )
        report_lines.append("")

        # --- Recommendations (Placeholder - could be expanded) ---
        report_lines.append("KEY RECOMMENDATIONS")
        report_lines.append("-" * 50)
        report_lines.append(
            f"• Focus marketing efforts on channels preferred by each persona."
        )
        report_lines.append(
            f"• Leverage personalized campaign copies for higher engagement and conversion."
        )
        report_lines.append(
            f"• Continuously analyze campaign performance against identified psychographics and channels."
        )
        report_lines.append("")

        return "\n".join(report_lines)

    @staticmethod
    def _generate_audience_segments(personas: List[Dict]) -> List[str]:
        """Helper to generate the audience segments part of the report."""
        segment_lines: List[str] = []
        if not personas:
            segment_lines.append("No audience personas found.")
            return segment_lines

        for i, persona in enumerate(personas, 1):
            name = persona.get("name", "Unnamed Persona").upper()
            description = persona.get("description", "No description provided.")
            psychographics = persona.get("psychographics", [])
            preferred_channels = persona.get("preferred_channels", [])

            segment_lines.append(f"{i}. {name}")
            segment_lines.append(f"   Description: {description}")

            if psychographics:
                segment_lines.append("   Psychographics:")
                for trait in psychographics:
                    segment_lines.append(f"   • {trait}")
            else:
                segment_lines.append("   Psychographics: Not specified.")

            if preferred_channels:
                segment_lines.append("   Preferred Channels:")
                for channel in preferred_channels:
                    segment_lines.append(f"   • {channel}")
            else:
                segment_lines.append("   Preferred Channels: Not specified.")
            segment_lines.append("")  # Add a blank line between personas
        return segment_lines

    @staticmethod
    def _generate_messaging_strategy(
        campaign_copies: List[Dict], personas: List[Dict]
    ) -> List[str]:
        """Helper to generate the messaging strategy part of the report."""
        messaging_lines: List[str] = []
        if not campaign_copies:
            messaging_lines.append("No campaign copies found.")
            return messaging_lines

        # Create a quick lookup for persona names
        persona_name_map = {
            p.get("persona_id"): p.get("name", "Unknown") for p in personas
        }

        for copy in campaign_copies:
            persona_id = copy.get("persona_id")
            persona_name = persona_name_map.get(persona_id, "Unknown Persona").upper()

            tagline = copy.get("tagline", "N/A")
            social_caption = copy.get("social_caption", "N/A")
            email_subject = copy.get("email_subject", "N/A")
            email_body = copy.get(
                "email_body", "N/A"
            )  # Assuming email_body might be available

            messaging_lines.append(f"{persona_name}:")
            messaging_lines.append(f"   Tagline: {tagline}")
            messaging_lines.append(f"   Social Media Caption: {social_caption}")
            messaging_lines.append(f"   Email Subject: {email_subject}")
            if email_body != "N/A":  # Only add if it's there
                messaging_lines.append(
                    f"   Email Body (Excerpt): {email_body[:100]}..."
                )  # Truncate for report
            messaging_lines.append("")  # Add a blank line between copies
        return messaging_lines
