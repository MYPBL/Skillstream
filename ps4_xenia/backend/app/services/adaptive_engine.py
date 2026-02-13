from sqlmodel import Session, select
from app.models.models import User, Asset, UserInteraction, AssetType, LearningStyle
from typing import Optional
import random

class AdaptiveEngine:
    def __init__(self, session: Session):
        self.session = session

    def calculate_performance_score(self, interaction: UserInteraction, asset: Asset) -> float:
        """
        Calculates a weighted performance score (0-100).
        - Quiz Score: 60% weight
        - Time Efficiency: 40% weight
        """
        raw_score = interaction.score if interaction.score is not None else 0.0
        
        # Time Factor: If completed faster than estimated, bonus. If slower, penalty.
        # Cap efficiency factor between 0.5 and 1.5
        efficiency_ratio = 1.0
        if interaction.time_spent_seconds > 0 and asset.estimated_duration_minutes > 0:
            estimated_seconds = asset.estimated_duration_minutes * 60
            efficiency_ratio = estimated_seconds / interaction.time_spent_seconds
        
        # Clamp efficiency
        efficiency_ratio = max(0.5, min(1.5, efficiency_ratio))
        
        # Normalize time factor to 0-100 scale (1.0 ratio = 80 pts, 1.5 = 100 pts, 0.5 = 40 pts)
        # Simple mapping: 1.0 -> 100% of the Time Component (which is 40pts total) ??
        # Let's simplify: 
        # Score component (max 60)
        score_component = (raw_score / 100.0) * 60.0
        
        # Time component (max 40)
        # If efficiency >= 1.0, full 40 pts. If 0.5, 20 pts.
        time_component = 40.0 * min(1.0, efficiency_ratio)
        
        total_score = score_component + time_component
        return total_score

    def recommend_next_asset(self, user_id: str, current_asset_id: Optional[str] = None) -> Optional[Asset]:
        """
        Determines the next asset for the user.
        """
        user = self.session.get(User, user_id)
        if not user:
            return None

        # Get user's history
        statement = select(UserInteraction).where(UserInteraction.user_id == user_id).order_by(UserInteraction.timestamp.desc())
        interactions = self.session.exec(statement).all()
        
        # Identify completed assets to exclude
        completed_asset_ids = {i.asset_id for i in interactions if i.status == "completed"}
        
        # If valid current_asset provided, analyze last interaction to adjust difficulty
        target_difficulty = 1 # Default
        target_type = None

        if interactions:
            last_interaction = interactions[0]
            last_asset = self.session.get(Asset, last_interaction.asset_id)
            
            if last_asset:
                perf_score = self.calculate_performance_score(last_interaction, last_asset)
                
                # Logic Tree
                if perf_score < 50:
                    # STRUGGLING: Reduce difficulty, maybe switch format
                    target_difficulty = max(1, last_asset.difficulty_level - 1)
                    # Switch format preference if they failed a text/video
                    if last_asset.content_type in ["video", "pdf", "html5"]:
                         target_type = "scorm" # Try interactive/sandbox if available
                elif perf_score > 90:
                    # ACCELERATING: Increase difficulty
                    target_difficulty = min(5, last_asset.difficulty_level + 1)
                else:
                    # STEADY: Keep same level
                    target_difficulty = last_asset.difficulty_level

        # Query for candidate assets
        query = select(Asset).where(Asset.id.notin_(completed_asset_ids))
        
        # Initial filtering by difficulty
        query = query.where(Asset.difficulty_level == target_difficulty)
        
        if target_type:
             query = query.where(Asset.content_type == target_type)
        
        candidates = self.session.exec(query).all()
        
        if not candidates:
            # Fallback: Relax constraints if no exact match
            query = select(Asset).where(Asset.id.notin_(completed_asset_ids))
            # Try just difficulty
            query_diff = query.where(Asset.difficulty_level == target_difficulty)
            candidates = self.session.exec(query_diff).all()
            
            if not candidates:
                 # Last resort: Any uncompleted asset
                 candidates = self.session.exec(query).all()
        
        if not candidates:
            return None # Course completed!

        # Return the best candidate (could be random or ordered by id)
        return candidates[0]

    def get_recommendations(self, user_id: str, limit: int = 3) -> list[Asset]:
        """
        Phase 6: Dynamic Path Adjustment.
        Uses Skill Mastery to Fast-Track (skip easy) or support (remedial) users.
        """
        user = self.session.get(User, user_id)
        if not user:
            return []

        # 1. Get user context
        statement = select(UserInteraction).where(UserInteraction.user_id == user_id).order_by(UserInteraction.timestamp.desc())
        interactions = self.session.exec(statement).all()
        completed_ids = {i.asset_id for i in interactions if i.status == "completed"}
        
        # 2. Get Skill Mastery
        from app.models.models import SkillMastery
        mastery_levels = self.session.exec(select(SkillMastery).where(SkillMastery.user_id == user_id)).all()
        mastered_skills = {m.skill_name for m in mastery_levels if m.proficiency > 80.0}
        struggling_skills = {m.skill_name for m in mastery_levels if m.proficiency < 40.0}

        # 3. Score Candidates
        query = select(Asset).where(Asset.id.notin_(completed_ids))
        candidates = self.session.exec(query).all()
        
        scored_candidates = []
        for asset in candidates:
            score = 0
            
            # --- PHASE 6 LOGIC START ---
            # A. Fast-Track Logic: If mastered, SKIP basic content
            if asset.skill_tag in mastered_skills and asset.difficulty_level <= 2:
                continue # Skip this asset, it's too easy for them
            
            # B. Remedial Logic: If struggling, BOOST basic content
            if asset.skill_tag in struggling_skills:
                if asset.difficulty_level <= 2:
                    score += 50 # Massive boost for remedial content
                elif asset.difficulty_level >= 4:
                    score -= 50 # Penalize hard content until basics are mastered
            # --- PHASE 6 LOGIC END ---

            # C. Difficulty Match (Max 30) - Adjusted from Phase 4
            # We still calculate "ideal" difficulty from last interaction, but it's secondary to Mastery now.
            # (Simplified for brevity, assuming Mastery overrides Micro-Performance)
            
            # D. Skill Match (Max 40)
            if asset.skill_tag in user.target_skills:
                score += 40
            elif asset.skill_tag in user.current_skills:
                score += 5
                
            # E. Learning Style Match (Max 10)
            preferred = user.preferred_learning_style
            if (preferred == "video" and asset.content_type == "video") or \
               (preferred == "text" and asset.content_type == "pdf") or \
               (preferred == "interactive" and asset.content_type in ["scorm", "html5"]):
                score += 10
            
            # F. Role Match (Max 10)
            if user.role and user.role.lower() in asset.skill_tag.lower():
                score += 10
                
            # G. Randomness (Max 5)
            score += random.randint(0, 5)
            
            scored_candidates.append((score, asset))
            
        # 4. Sort and Return
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        
        # 5. Check for Automatic Notifications (Stub for now)
        # In a real event-bus system, we'd trigger a notification if we skipped content.
        
        return [item[1] for item in scored_candidates[:limit]]
