"""
This file contains the logic to copy and update the year data for all flowchart templates from the recent year to a new year folder.
"""

import json
from pathlib import Path

def main():
    """
    Reads the latest year folder and creates a new one.
    Copies over all templates from the prior recent year to the new one, updating year info in the process.W
    """

    # Creates the flowchart templates path
    templates_directory = "json/templates"
    templates_path = Path(templates_directory)

    # Gets the name of the most recent year folder
    recent_year_path = list(p for p in templates_path.iterdir() if p.is_dir())[-1]
    recent_year_name = recent_year_path.name
    recent_year_name_underscore = recent_year_name.replace("-", "_")

    # Gets the recent end year and declares the next year folder
    recent_end_year = int(recent_year_name.split("-")[1])
    new_year_name = f"{recent_end_year}-{recent_end_year + 1}"
    new_year_name_underscore = f"{recent_end_year}_{recent_end_year + 1}"

    # Creates the new year folder under templates
    new_year_path = Path(f"{templates_directory}/{new_year_name}")
    new_year_path.mkdir()

    # Copies the flowchart file from the recent year to the new year, updates its year info
    for flowchart_path in recent_year_path.iterdir():
        with open(flowchart_path, "r") as flowchart_file:
            flowchart_path = flowchart_file.name
            flowchart_name = flowchart_path.split("\\")[3].replace(recent_year_name_underscore, new_year_name_underscore)
            flowchart = json.load(flowchart_file)
            flowchart["title"] = flowchart["title"].replace(recent_year_name, new_year_name)
            with open(f"{templates_directory}/{new_year_name}/{flowchart_name}", "x") as new_flowchart:
                json.dump(flowchart, new_flowchart)


if __name__ == "__main__":
    main()
