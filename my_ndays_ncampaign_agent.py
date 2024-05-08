from adx.agents import NDaysNCampaignsAgent
from adx.tier1_ndays_ncampaign_agent import Tier1NDaysNCampaignsAgent
from adx.adx_game_simulator import AdXGameSimulator
from adx.structures import Bid, Campaign, BidBundle 
from typing import Set, Dict

class MyNDaysNCampaignsAgent(NDaysNCampaignsAgent):

    def __init__(self):
        # TODO: fill this in (if necessary)
        super().__init__()
        self.name = "Bajas #1"  # DONE: enter a name.
        self.b_a =  3.08577 / 4.08577 + 0.1 # b/a, optimal for second derivative test
        self.threshold = 0.5
        self.discount_factor = 0.5

    def on_new_game(self) -> None:
        # TODO: fill this in (if necessary)
        pass

    def get_ad_bids(self) -> Set[BidBundle]:
        # TODO: fill this in
        bundles = set()
        for campaign in self.get_active_campaigns():
            effective_budget = campaign.budget - self.get_cumulative_cost(campaign)
            effective_reach = campaign.reach - self.get_cumulative_reach(campaign)
            
            if effective_reach == 0:
                bid_per_item = 0
            else:
                factor = self.b_a if self.current_day >= 4 else 1
                bid_per_item = factor * (effective_budget) / (effective_reach)

            quality_score = self.get_quality_score()
            print(f"Effective Budget: {effective_budget}, Effective Reach: {effective_reach}, Bid per Item: {bid_per_item}, Quality Score: {quality_score}")
            
            bid_entries = set()
            bid_entries.add(Bid(bidder=self, auction_item=campaign.target_segment, bid_per_item=bid_per_item, bid_limit=effective_budget))
            
            bundle = BidBundle(campaign_id=campaign.uid, limit=effective_budget, bid_entries=bid_entries)
            bundles.add(bundle)

        return bundles
    
    def get_campaign_bids(self, campaigns_for_auction:  Set[Campaign]) -> Dict[Campaign, float]:
        # TODO: fill this in
        current_day = self.current_day
        # for campaign in campaigns_for_auction:
            # print(campaign.start_day - current_day == 1)

        return {}
        # # Current Strategy: Not bidding on any other campaigns! Focusing on completing our current ones
        # bids = {}
        # for campaign in campaigns_for_auction:
        #     if (campaign.budget / campaign.reach) > self.threshold:
        #         bid_value = (campaign.budget) * self.discount_factor
        #         bids[campaign] = bid_value
        # return bids

if __name__ == "__main__":
    # Here's an opportunity to test offline against some TA agents. Just run this file to do so.
    test_agents = [MyNDaysNCampaignsAgent()] + [Tier1NDaysNCampaignsAgent(name=f"Agent {i + 1}") for i in range(9)]

    # Don't change this. Adapt initialization to your environment
    simulator = AdXGameSimulator()
    simulator.run_simulation(agents=test_agents, num_simulations=100)