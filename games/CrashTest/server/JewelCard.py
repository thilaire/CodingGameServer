from dataclasses import dataclass

@dataclass
class JewelCard:
    """Base class for Jewel Cards. Each jewel card will be an instance of this class."""
    tokenType: int|None # see Constants.py
    nbJewel: int        # 0,1,2
    nbPrestige: int     # 0,1,2,6
    nbCrowns: int       # 0,1,2
