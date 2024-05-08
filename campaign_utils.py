from adx.structures import Campaign, MarketSegment
from adx.adx_game_simulator import CONFIG, calculate_effective_reach
import numpy as np

# '''
# Helps us track ongoing campaigns and their associated statuses. We will use this
# to track ongoing campaigns. 
# '''
# class CampaignTracker:
#     def __init__(self):
#         self.pending_auctions = []  # these auctions will take place in the next day
#         self.current_auctions = []  # these auctions are ongoing

#     def update_auctions(self, day):
#         self.current_auctions += self.pending_auctions
#         self.pending_auctions.clear()
#         for campaign in self.current_auctions:
#             if campaign.end_day < day: # if ended
#                 self.current_auctions.remove(campaign)

#     def add_to_pending(self, campaign):
#         self.pending_auctions.append(campaign)

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

def get_competitor_segments(base_set):
    biddable_segments = set()
    for segment, attributes in segment_dict.items():
        if attributes.intersection(base_set) == attributes:  # ensures all attributes of 'segment' are in 'base_set'
            biddable_segments.add(segment)
    return biddable_segments


def campaign_shade(my_campaign : Campaign, allCampaigns : list[Campaign]):
    my_shade = 1 / (my_campaign.end_day - my_campaign.start_day + 1)

    my_segment = my_campaign.target_segment
    competitors = get_competitor_segments(my_segment)
    cumulative_reach = 0
    possible_total_reach = 0
    for campaign in allCampaigns:            
        if campaign.target_segment in competitors:
            # less reach per day if longer campaign
            day_factor = 1 / (campaign.end_day - campaign.start_day + 1)
            reach_remaining = campaign.reach - campaign.cumulative_reach
            cumulative_reach += reach_remaining * day_factor
            possible_total_reach += reach_remaining
    general_shade = cumulative_reach / possible_total_reach if possible_total_reach != 0 else 0

    shade = (3 * my_shade + 2 * general_shade) / 5

    my_effective_reach = calculate_effective_reach(my_campaign.cumulative_reach, my_campaign.reach)

    if my_effective_reach == 0:
        # we have no effective reach
        return shade

    count = 0
    sum_other_effective_reach = 0
    for other_campaign in allCampaigns:
        if other_campaign.target_segment in competitors and other_campaign != my_campaign:
            count += 1
            other_effective_reach = calculate_effective_reach(other_campaign.cumulative_reach, other_campaign.reach)
            sum_other_effective_reach += other_effective_reach
    
    if count == 0 or sum_other_effective_reach == 0:
        # edge case where we are the only campaign for this market segment
        return shade
    
    average_other_effective_reach = sum_other_effective_reach / count

    if my_effective_reach < average_other_effective_reach:
        # we have low effective reach, we need more impressions, bid more
        return shade
    else:
        # we have high effective reach, we already doing fine, bid less
        return shade * (average_other_effective_reach / my_effective_reach)
