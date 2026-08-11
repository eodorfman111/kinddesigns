"""
Illustrative per-site data for the Kind Designs pitch demo.

These are NOT real survey results — Kind Designs' actual FIU/Harborne-lab
monitoring data is private and unpublished. Site names and approximate
locations are real (pulled from kinddesigns.com and press coverage);
species lists, counts, and diversity indices are plausible placeholder
numbers meant to show what the dashboard would look like once real GoPro
footage is run through the pipeline. Every place this data surfaces in the
app says so explicitly — see app.py.
"""

SITES = [
    {
        "name": "Pine Tree Dr",
        "area": "Miami Beach",
        "lat": 25.8237, "lon": -80.1332,
        "installed": 2024,
        "months_monitored": 18,
        "species": ["Sheepshead", "French Grunt", "Gray Snapper", "Sergeant Major"],
        "invertebrates": ["Barnacles", "Tunicates", "Oysters"],
        "diversity_index": 0.71,
        "fish_count_avg": 34,
    },
    {
        "name": "North Bay Road",
        "area": "Miami Beach",
        "lat": 25.8102, "lon": -80.1408,
        "installed": 2024,
        "months_monitored": 14,
        "species": ["Sergeant Major", "Gray Snapper", "Pinfish", "Mullet"],
        "invertebrates": ["Tunicates", "Bryozoans", "Mussels"],
        "diversity_index": 0.68,
        "fish_count_avg": 29,
    },
    {
        "name": "Venetian Island",
        "area": "Miami Beach",
        "lat": 25.7909, "lon": -80.1631,
        "installed": 2025,
        "months_monitored": 8,
        "species": ["French Grunt", "Sheepshead", "Blue Tang"],
        "invertebrates": ["Barnacles", "Oyster Toadfish Habitat"],
        "diversity_index": 0.58,
        "fish_count_avg": 21,
    },
    {
        "name": "Palm Island",
        "area": "Miami Beach",
        "lat": 25.7809, "lon": -80.1573,
        "installed": 2025,
        "months_monitored": 6,
        "species": ["Sergeant Major", "Pinfish"],
        "invertebrates": ["Barnacles"],
        "diversity_index": 0.44,
        "fish_count_avg": 15,
    },
    {
        "name": "Star Island",
        "area": "Miami Beach",
        "lat": 25.7797, "lon": -80.1516,
        "installed": 2025,
        "months_monitored": 6,
        "species": ["Gray Snapper", "French Grunt"],
        "invertebrates": ["Tunicates"],
        "diversity_index": 0.49,
        "fish_count_avg": 18,
    },
    {
        "name": "Sunset Islands",
        "area": "Miami Beach",
        "lat": 25.8127, "lon": -80.1447,
        "installed": 2025,
        "months_monitored": 4,
        "species": ["Sheepshead", "Mullet"],
        "invertebrates": ["Barnacles", "Bryozoans"],
        "diversity_index": 0.38,
        "fish_count_avg": 11,
    },
    {
        "name": "Bayfront Park",
        "area": "Miami Shores Village",
        "lat": 25.8737, "lon": -80.1889,
        "installed": 2026,
        "months_monitored": 1,
        "species": ["Pinfish"],
        "invertebrates": ["Barnacles"],
        "diversity_index": 0.21,
        "fish_count_avg": 5,
    },
    {
        "name": "Bryan Place",
        "area": "Fort Lauderdale",
        "lat": 26.1224, "lon": -80.1373,
        "installed": 2025,
        "months_monitored": 5,
        "species": ["Sergeant Major", "Gray Snapper", "French Grunt"],
        "invertebrates": ["Tunicates", "Mussels"],
        "diversity_index": 0.52,
        "fish_count_avg": 19,
    },
]
