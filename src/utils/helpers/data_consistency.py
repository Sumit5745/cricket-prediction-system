"""
Data consistency module for cricket prediction system.
This module ensures data consistency across the system.
"""
import logging
from typing import Dict, List, Any, Optional, Union, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataConsistency:
    """
    Ensures data consistency across the cricket prediction system.
    """
    
    @staticmethod
    def ensure_batting_consistency(batting_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure batting data consistency.
        
        Args:
            batting_data: Batting data dictionary
            
        Returns:
            Consistent batting data
        """
        # Extract key metrics
        runs = batting_data.get('expected_runs', 0)
        balls = batting_data.get('expected_balls', 0)
        strike_rate = batting_data.get('expected_strike_rate', 0)
        fours = batting_data.get('expected_fours', 0)
        sixes = batting_data.get('expected_sixes', 0)
        
        # Ensure mathematical consistency
        
        # 1. Strike rate = (runs / balls) * 100
        if balls > 0:
            strike_rate = (runs / balls) * 100
        elif strike_rate > 0:
            balls = (runs / strike_rate) * 100
        
        # 2. Ensure boundary runs don't exceed total runs
        boundary_runs = (fours * 4) + (sixes * 6)
        if boundary_runs > runs:
            # Scale down boundaries proportionally
            scale_factor = runs / max(1, boundary_runs)
            fours = fours * scale_factor
            sixes = sixes * scale_factor
        
        # 3. Ensure non-zero values for key metrics
        runs = max(0, runs)
        balls = max(1, balls)
        strike_rate = max(0, strike_rate)
        fours = max(0, fours)
        sixes = max(0, sixes)
        
        # Update data
        batting_data.update({
            'expected_runs': round(runs, 1),
            'expected_balls': round(balls, 1),
            'expected_strike_rate': round(strike_rate, 1),
            'expected_fours': round(fours, 1),
            'expected_sixes': round(sixes, 1)
        })
        
        return batting_data
    
    @staticmethod
    def ensure_bowling_consistency(bowling_data: Dict[str, Any], format_type: str = 'T20I') -> Dict[str, Any]:
        """
        Ensure bowling data consistency.
        
        Args:
            bowling_data: Bowling data dictionary
            format_type: Match format
            
        Returns:
            Consistent bowling data
        """
        # Extract key metrics
        overs = bowling_data.get('expected_overs', 0)
        economy = bowling_data.get('expected_economy', 0)
        wickets = bowling_data.get('expected_wickets', 0)
        runs_conceded = bowling_data.get('expected_runs_conceded', 0)
        
        # Ensure mathematical consistency
        
        # 1. Runs conceded = economy * overs
        if overs > 0 and economy > 0:
            runs_conceded = economy * overs
        elif runs_conceded > 0 and overs > 0:
            economy = runs_conceded / overs
        
        # 2. Ensure format-specific constraints
        if format_type.upper() == 'T20I':
            overs = min(overs, 4)  # Max 4 overs in T20
        elif format_type.upper() == 'ODI':
            overs = min(overs, 10)  # Max 10 overs in ODI
        
        # 3. Ensure non-zero values for key metrics
        overs = max(0, overs)
        economy = max(0, economy)
        wickets = max(0, wickets)
        runs_conceded = max(0, runs_conceded)
        
        # Update data
        bowling_data.update({
            'expected_overs': round(overs, 1),
            'expected_economy': round(economy, 1),
            'expected_wickets': round(wickets, 1),
            'expected_runs_conceded': round(runs_conceded, 1)
        })
        
        return bowling_data
    
    @staticmethod
    def ensure_player_role_consistency(player_data: Dict[str, Any], prediction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure player role consistency in predictions.
        
        Args:
            player_data: Player data dictionary
            prediction: Player prediction dictionary
            
        Returns:
            Consistent player prediction
        """
        # Get player role
        role = player_data.get('personalInformation', {}).get('role', '').lower()
        
        # Adjust prediction based on role
        if 'batsman' in role:
            # Specialist batsmen should have higher expected runs
            if 'batting' in prediction:
                runs = prediction['batting'].get('expected_runs', 0)
                if runs < 20:
                    prediction['batting']['expected_runs'] = max(runs, 20)
            
            # Specialist batsmen should not be predicted to take wickets
            if 'bowling' in prediction:
                wickets = prediction['bowling'].get('expected_wickets', 0)
                if wickets > 0.5:
                    prediction['bowling']['expected_wickets'] = min(wickets, 0.5)
        elif 'bowler' in role:
            # Specialist bowlers should have lower expected runs
            if 'batting' in prediction:
                runs = prediction['batting'].get('expected_runs', 0)
                if runs > 15:
                    prediction['batting']['expected_runs'] = min(runs, 15)
            
            # Specialist bowlers should have higher expected wickets
            if 'bowling' in prediction:
                wickets = prediction['bowling'].get('expected_wickets', 0)
                if wickets < 1:
                    prediction['bowling']['expected_wickets'] = max(wickets, 1)
        elif 'all-rounder' in role or 'all rounder' in role:
            # All-rounders should have moderate expected runs and wickets
            if 'batting' in prediction:
                runs = prediction['batting'].get('expected_runs', 0)
                if runs < 15:
                    prediction['batting']['expected_runs'] = max(runs, 15)
            
            if 'bowling' in prediction:
                wickets = prediction['bowling'].get('expected_wickets', 0)
                if wickets < 0.5:
                    prediction['bowling']['expected_wickets'] = max(wickets, 0.5)
        
        return prediction
    
    @staticmethod
    def ensure_fantasy_team_consistency(fantasy_team: Dict[str, Any], format_type: str = 'T20I') -> Dict[str, Any]:
        """
        Ensure fantasy team consistency.
        
        Args:
            fantasy_team: Fantasy team dictionary
            format_type: Match format
            
        Returns:
            Consistent fantasy team
        """
        # Ensure we have exactly 11 players
        players = fantasy_team.get('players', [])
        if len(players) != 11:
            logger.warning(f"Fantasy team has {len(players)} players instead of 11")
        
        # Ensure captain and vice-captain are in the team
        captain = fantasy_team.get('captain', '')
        vice_captain = fantasy_team.get('vice_captain', '')
        
        captain_in_team = any(p.get('name', '') == captain for p in players)
        vice_captain_in_team = any(p.get('name', '') == vice_captain for p in players)
        
        if not captain_in_team and players:
            logger.warning(f"Captain {captain} not in team, setting first player as captain")
            fantasy_team['captain'] = players[0].get('name', '')
        
        if not vice_captain_in_team and len(players) > 1:
            logger.warning(f"Vice-captain {vice_captain} not in team, setting second player as vice-captain")
            fantasy_team['vice_captain'] = players[1].get('name', '')
        
        # Ensure player performances are consistent
        for player in players:
            performance = player.get('performance', {})
            
            # Ensure batting consistency
            if 'batting' in performance:
                performance['batting'] = DataConsistency.ensure_batting_consistency(performance['batting'])
            
            # Ensure bowling consistency
            if 'bowling' in performance:
                performance['bowling'] = DataConsistency.ensure_bowling_consistency(performance['bowling'], format_type)
        
        return fantasy_team
    
    @staticmethod
    def ensure_match_prediction_consistency(match_prediction: Dict[str, Any], format_type: str = 'T20I') -> Dict[str, Any]:
        """
        Ensure match prediction consistency.
        
        Args:
            match_prediction: Match prediction dictionary
            format_type: Match format
            
        Returns:
            Consistent match prediction
        """
        # Ensure win probabilities sum to 1
        team_probs = match_prediction.get('prediction', {}).get('team_probabilities', {})
        if team_probs:
            teams = list(team_probs.keys())
            if len(teams) == 2:
                team1, team2 = teams
                prob1 = team_probs.get(team1, 0.5)
                prob2 = team_probs.get(team2, 0.5)
                
                # Normalize probabilities
                total_prob = prob1 + prob2
                if total_prob > 0:
                    prob1 = prob1 / total_prob
                    prob2 = prob2 / total_prob
                else:
                    prob1 = 0.5
                    prob2 = 0.5
                
                # Update probabilities
                team_probs[team1] = round(prob1, 3)
                team_probs[team2] = round(prob2, 3)
                
                # Update win probability
                match_prediction['prediction']['win_probability'] = round(max(prob1, prob2), 3)
        
        # Ensure expected scores are realistic for the format
        expected_scores = match_prediction.get('expected_scores', {})
        if expected_scores:
            for team, score in expected_scores.items():
                if format_type.upper() == 'T20I':
                    # T20 scores typically range from 120-220
                    expected_scores[team] = max(120, min(score, 220))
                elif format_type.upper() == 'ODI':
                    # ODI scores typically range from 200-350
                    expected_scores[team] = max(200, min(score, 350))
        
        return match_prediction