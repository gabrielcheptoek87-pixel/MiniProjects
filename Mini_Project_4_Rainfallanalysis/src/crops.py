"""Crop rainfall rules and month-by-month suitability classification."""
from .data import REGIONS


class CropRule:
    """Suitable monthly rainfall band [good_min, good_max] (mm) for a crop,
    plus the threshold above which a month is a waterlogging risk.

    below good_min -> "Drought risk"; above waterlog_max -> "Waterlogging
    risk"; between good_max and waterlog_max -> "Marginal (wet)";
    inside [good_min, good_max] -> "Good for <crop>".
    """

    def __init__(self, crop, good_min, good_max, waterlog_max, source):
        self.crop = crop
        self.good_min = good_min
        self.good_max = good_max
        self.waterlog_max = waterlog_max
        self.source = source

    def classify(self, mm):
        if mm < self.good_min:
            return "Drought risk"
        if mm > self.waterlog_max:
            return "Waterlogging risk"
        if mm > self.good_max:
            return "Marginal (wet)"
        return f"Good for {self.crop}"


# Maize: rainfed maize ~600-900 mm/yr (~50-75 mm/month, more at mid-season).
#   Tekwa & Bwade (2011), CIGR Journal 13(1), citing Arora (2004).
# Beans: 350-500 mm over a 3-4 month season; unsuited to humid wet tropics.
#   Bioversity/CIAT bean regeneration guidelines; FAO Land & Water Bean sheet.
# Coffee (Robusta): 1200-1500 mm/yr well distributed over ~9 months,
#   tolerating a dry spell of up to ~3 months.
#   NARO/NaCRRI Uganda (2010), "Establishment and Field Management of Robusta Coffee".
CROP_RULES = {
    "maize": CropRule(
        "maize", good_min=50, good_max=150, waterlog_max=180,
        source="Tekwa & Bwade (2011), CIGR Journal 13(1), citing Arora (2004): "
               "rainfed maize ~600-900 mm/annum (~50-75 mm/month, more at mid-season)."),
    "beans": CropRule(
        "beans", good_min=40, good_max=120, waterlog_max=150,
        source="Bioversity International/CIAT bean regeneration guidelines "
               "(350-500 mm over a 3-4 month season); FAO Land & Water Bean "
               "crop sheet (not suited to humid wet tropics)."),
    "coffee": CropRule(
        "coffee", good_min=60, good_max=190, waterlog_max=250,
        source="NARO/NaCRRI Uganda (2010), Robusta Coffee: 1200-1500 mm/year, "
               "well distributed over ~9 months, tolerating a dry spell of ~3 months."),
}


def classify_all(regions=None, rules=None):
    """Nested dict: region -> crop -> list of 12 classification strings."""
    regions = regions or REGIONS
    rules = rules or CROP_RULES
    return {
        rname: {cname: [rule.classify(mm) for mm in region.rainfall]
                for cname, rule in rules.items()}
        for rname, region in regions.items()
    }


def simplify_label(label):
    """Collapse 'Good for maize' etc. to 'Good' for plotting."""
    return "Good" if label.startswith("Good") else label
