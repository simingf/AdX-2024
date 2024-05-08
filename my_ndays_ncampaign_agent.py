from adx.agents import NDaysNCampaignsAgent
from adx.tier1_ndays_ncampaign_agent import Tier1NDaysNCampaignsAgent
from adx.adx_game_simulator import AdXGameSimulator, CONFIG
from adx.structures import Bid, Campaign, BidBundle, MarketSegment 
from typing import Set, Dict
import numpy as np
import campaign_utils

class MyNDaysNCampaignsAgent(NDaysNCampaignsAgent):

    def __init__(self):
        # TODO: fill this in (if necessary)
        super().__init__()
        self.name = "Bajas #1"  # DONE: enter a name.
        self.campaign_tracker = campaign_utils.CampaignTracker()

    def on_new_game(self) -> None:
        # TODO: fill this in (if necessary)
        pass

    def get_ad_bids(self) -> Set[BidBundle]:
        # TODO: fill this in
        bundles = set()
        current_day = self.current_day

        # Get counts for how often a given segment appears in active campaigns.
        overlappingSegments = {}
        for campaign in self.get_active_campaigns():
            competitors = campaign_utils.competitor_segments(campaign.target_segment)
            for segment in competitors:
                if segment in overlappingSegments:
                    overlappingSegments[segment] += 1
                else:
                    overlappingSegments[segment] = 1

        # Get the value of each segment.
        segmentValues = {}
        for segment in overlappingSegments:
            segmentValues[segment] = campaign_utils.segment_value(segment, self.get_active_campaigns())

        for campaign in self.get_active_campaigns():
            effective_budget = campaign.budget - self.get_cumulative_cost(campaign)
            effective_reach = campaign.reach - self.get_cumulative_reach(campaign)
            bid_per_item = segmentValues[campaign.target_segment] * (effective_budget) / (effective_reach) if effective_reach != 0 else 0

            quality_score = self.get_quality_score()
            print(f"Effective Budget: {effective_budget}, Effective Reach: {effective_reach}, Bid per Item: {bid_per_item}, Quality Score: {quality_score}")
            
            bid_entries = set()
            bid_entries.add(Bid(bidder=self, auction_item=campaign.target_segment, bid_per_item=bid_per_item, bid_limit=effective_budget))
            
            bundle = BidBundle(campaign_id=campaign.uid, limit=effective_budget, bid_entries=bid_entries)
            bundles.add(bundle)
        return bundles
    
    def get_campaign_bids(self, campaigns_for_auction:  Set[Campaign]) -> Dict[Campaign, float]:
        # Simple approach: bid a shaded portion for each campaign. 
        self.campaign_tracker.update_auctions(self.current_day)
        bids = {}
        for campaign in campaigns_for_auction:
            market_segment = campaign.target_segment
            market_segment_population = CONFIG['market_segment_pop'][market_segment]
            percentage_of_population = campaign.reach / market_segment_population
            if abs(percentage_of_population - 0.3) < 0.01:
                shading = 0.8 / self.quality_score
            elif abs(percentage_of_population - 0.5) < 0.01:
                shading = 0.9 / self.quality_score
            elif abs(percentage_of_population - 0.7) < 0.01:
                shading = 1 / self.quality_score
            else:
                # ERROR SHOULD NOT BE HERE
                print("SHOULD NOT REACH")
                shading = 1 / self.quality_score
            bid = campaign.reach * shading
            bids[campaign] = bid
        return bids

if __name__ == "__main__":
    # Here's an opportunity to test offline against some TA agents. Just run this file to do so.
    test_agents = [MyNDaysNCampaignsAgent()] + [Tier1NDaysNCampaignsAgent(name=f"Agent {i + 1}") for i in range(9)]

    # Don't change this. Adapt initialization to your environment
    simulator = AdXGameSimulator()
    simulator.run_simulation(agents=test_agents, num_simulations=100)