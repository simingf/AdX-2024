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

    def update_auctions(self, ):
        self.current_auctions += self.pending_auctions
        self.pending_auctions.clear()
        for campaign in self.current_auctions:
            # if campaign.
            pass