from dataclasses import dataclass, field

@dataclass
class JewelCard:
    """Base class for Jewel Cards. Each jewel card will be an instance of this class."""
    tokenType: int|None # see Constants.py
    nbJewel: int        # 0,1,2
    nbPrestige: int     # 0,1,2,5,6
    nbCrowns: int       # 0,1,2,3
    #abilities: str     # maybe a list of strings would be better? Probably, there's an instance of a card w/ two abilities...
    #requirements: list[int|None] = field(default_factory = lambda : [0, 0, 0, 0, 0, 0])    #[None, Sapphire, diamond, emerald, ruby, obsidian]
                                                                                            #should be replaced w/ a dict?

