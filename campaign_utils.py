from adx.structures import Campaign, MarketSegment
from adx.adx_game_simulator import CONFIG

'''
Helps us track ongoing campaigns and their associated statuses. We will use this
to track ongoing campaigns. 
'''
class CampaignTracker:
    def __init__(self):
        self.pending_auctions = []  # these auctions will take place in the next day
        self.current_auctions = []  # these auctions are ongoing

    def update_auctions(self, day):
        self.current_auctions += self.pending_auctions
        self.pending_auctions.clear()
        for campaign in self.current_auctions:
            if campaign.end_day < day: # if ended
                self.current_auctions.remove(campaign)

    def add_to_pending(self, campaign):
        self.pending_auctions.append(campaign)

segment_dict = {
        MarketSegment(("Male", "Young")): {"Male", "Young"},
        MarketSegment(("Male", "Old")): {"Male", "Old"},
        MarketSegment(("Male", "LowIncome")): {"Male", "LowIncome"},
        MarketSegment(("Male", "HighIncome")): {"Male", "HighIncome"},
        MarketSegment(("Female", "Young")): {"Female", "Young"},
        MarketSegment(("Female", "Old")): {"Female", "Old"},
        MarketSegment(("Female", "LowIncome")): {"Female", "LowIncome"},
        MarketSegment(("Female", "HighIncome")): {"Female", "HighIncome"},
        MarketSegment(("Young", "LowIncome")): {"Young", "LowIncome"},
        MarketSegment(("Old", "LowIncome")): {"Old", "LowIncome"},
        MarketSegment(("Young", "HighIncome")): {"Young", "HighIncome"},
        MarketSegment(("Old", "HighIncome")): {"Old", "HighIncome"},
        MarketSegment(("Male", "Young", "LowIncome")): {"Male", "Young", "LowIncome"},
        MarketSegment(("Female", "Young", "LowIncome")): {"Female", "Young", "LowIncome"},
        MarketSegment(("Male", "Old", "LowIncome")): {"Male", "Old", "LowIncome"},
        MarketSegment(("Male", "Young", "HighIncome")): {"Male", "Young", "HighIncome"},
        MarketSegment(("Female", "Old", "LowIncome")): {"Female", "Old", "LowIncome"},
        MarketSegment(("Female", "Young", "HighIncome")): {"Female", "Young", "HighIncome"},
        MarketSegment(("Male", "Old", "HighIncome")): {"Male", "Old", "HighIncome"},
        MarketSegment(("Female", "Old", "HighIncome")): {"Female", "Old", "HighIncome"}
    }

def competitor_segments(base_set):
    biddable_segments = set()
    for segment, attributes in segment_dict.items():
        if attributes.intersection(base_set) == attributes:  # ensures all attributes of 'segment' are in 'base_set'
            biddable_segments.add(segment)
    return biddable_segments

def segment_value(segment : MarketSegment, allCampaigns : list[Campaign]): # represents a segment's worth
    cumulative_reach = 0
    possible_total_reach = 0
    competitors = competitor_segments(segment)
    for campaign in allCampaigns:
        if campaign.target_segment in competitors:
            day_factor = 1 / (campaign.end_day - campaign.start_day + 1) # less reach per day if longer campaign
            cumulative_reach += campaign.reach * day_factor
            possible_total_reach += campaign.reach
    return cumulative_reach / possible_total_reach if possible_total_reach != 0 else 0