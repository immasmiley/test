"""
SphereOS Value Streaming System
Streams and matches value content to users
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class ContentType(Enum):
    ARTICLE = "article"
    VIDEO = "video"
    PODCAST = "podcast"
    COURSE = "course"
    EVENT = "event"
    TOOL = "tool"
    NETWORK = "network"


class ValueCategory(Enum):
    PROFESSIONAL = "professional"
    PERSONAL = "personal"
    FINANCIAL = "financial"
    SOCIAL = "social"
    EDUCATIONAL = "educational"
    HEALTH = "health"
    CREATIVE = "creative"


@dataclass
class ValueContent:
    content_id: str
    title: str
    description: str
    content_type: ContentType
    value_category: ValueCategory
    value_score: float
    tags: List[str]
    author: str
    url: Optional[str] = None
    duration_minutes: Optional[int] = None
    created_at: str = None


@dataclass
class UserValueProfile:
    user_npub: str
    interests: List[str]
    value_preferences: Dict[ValueCategory, float]
    skill_levels: Dict[str, float]
    location: Optional[str] = None
    time_availability: Optional[str] = None
    created_at: str = None


@dataclass
class ValueMatch:
    match_id: str
    user_npub: str
    content_id: str
    match_score: float
    relevance_factors: List[str]
    created_at: str = None


class ValueStreamingSystem:
    """Main value streaming system"""
    
    def __init__(self):
        self.content_database: List[ValueContent] = []
        self.user_profiles: Dict[str, UserValueProfile] = {}
        self.value_matches: List[ValueMatch] = []
        self._initialize_sample_content()
    
    def _initialize_sample_content(self):
        """Initialize with sample value content"""
        sample_content = [
            ValueContent(
                content_id="content_001",
                title="Advanced Python Programming",
                description="Learn advanced Python techniques for professional development",
                content_type=ContentType.COURSE,
                value_category=ValueCategory.PROFESSIONAL,
                value_score=8.5,
                tags=["python", "programming", "professional"],
                author="Tech Expert",
                created_at=datetime.now().isoformat(),
                duration_minutes=120
            ),
            ValueContent(
                content_id="content_002",
                title="Networking Strategies for Entrepreneurs",
                description="Build meaningful professional relationships",
                content_type=ContentType.ARTICLE,
                value_category=ValueCategory.SOCIAL,
                value_score=7.8,
                tags=["networking", "entrepreneurship", "social"],
                author="Business Coach",
                created_at=datetime.now().isoformat()
            ),
            ValueContent(
                content_id="content_003",
                title="Financial Planning Basics",
                description="Essential financial planning for beginners",
                content_type=ContentType.VIDEO,
                value_category=ValueCategory.FINANCIAL,
                value_score=8.2,
                tags=["finance", "planning", "beginners"],
                author="Financial Advisor",
                created_at=datetime.now().isoformat(),
                duration_minutes=45
            )
        ]
        self.content_database.extend(sample_content)
    
    async def get_value_feeds(self) -> List[ValueContent]:
        """Get all available value content"""
        return self.content_database
    
    async def fetch_value_content(self, content_type: Optional[ContentType] = None,
                                value_category: Optional[ValueCategory] = None,
                                min_value_score: float = 0.0) -> List[ValueContent]:
        """Fetch value content with filters"""
        filtered_content = []
        
        for content in self.content_database:
            if content_type and content.content_type != content_type:
                continue
            if value_category and content.value_category != value_category:
                continue
            if content.value_score < min_value_score:
                continue
            
            filtered_content.append(content)
        
        # Sort by value score
        filtered_content.sort(key=lambda x: x.value_score, reverse=True)
        return filtered_content
    
    async def create_user_value_profile(self, user_npub: str, interests: List[str],
                                      value_preferences: Dict[str, float],
                                      skill_levels: Dict[str, float],
                                      location: str = None) -> UserValueProfile:
        """Create or update user value profile"""
        
        # Convert string preferences to enum
        enum_preferences = {}
        for category_str, score in value_preferences.items():
            try:
                category_enum = ValueCategory(category_str)
                enum_preferences[category_enum] = score
            except ValueError:
                continue
        
        profile = UserValueProfile(
            user_npub=user_npub,
            interests=interests,
            value_preferences=enum_preferences,
            skill_levels=skill_levels,
            location=location,
            created_at=datetime.now().isoformat()
        )
        
        self.user_profiles[user_npub] = profile
        return profile
    
    async def get_user_value_matches(self, user_npub: str, limit: int = 20) -> List[ValueMatch]:
        """Get value matches for a user"""
        if user_npub not in self.user_profiles:
            return []
        
        profile = self.user_profiles[user_npub]
        matches = []
        
        for content in self.content_database:
            match_score = self._calculate_match_score(profile, content)
            
            if match_score > 0.5:  # Only include relevant matches
                match = ValueMatch(
                    match_id=f"match_{user_npub}_{content.content_id}",
                    user_npub=user_npub,
                    content_id=content.content_id,
                    match_score=match_score,
                    relevance_factors=self._get_relevance_factors(profile, content),
                    created_at=datetime.now().isoformat()
                )
                matches.append(match)
        
        # Sort by match score and limit results
        matches.sort(key=lambda x: x.match_score, reverse=True)
        return matches[:limit]
    
    def _calculate_match_score(self, profile: UserValueProfile, content: ValueContent) -> float:
        """Calculate match score between user profile and content"""
        score = 0.0
        
        # Interest matching
        interest_matches = sum(1 for interest in profile.interests if interest.lower() in [tag.lower() for tag in content.tags])
        if profile.interests:
            interest_score = interest_matches / len(profile.interests)
            score += interest_score * 0.4
        
        # Value category preference
        if content.value_category in profile.value_preferences:
            category_score = profile.value_preferences[content.value_category]
            score += category_score * 0.3
        
        # Content value score
        score += content.value_score * 0.2
        
        # Skill level matching
        skill_matches = sum(1 for skill in profile.skill_levels if skill.lower() in [tag.lower() for tag in content.tags])
        if profile.skill_levels:
            skill_score = skill_matches / len(profile.skill_levels)
            score += skill_score * 0.1
        
        return min(score, 1.0)
    
    def _get_relevance_factors(self, profile: UserValueProfile, content: ValueContent) -> List[str]:
        """Get factors that make content relevant to user"""
        factors = []
        
        # Interest matches
        for interest in profile.interests:
            if interest.lower() in [tag.lower() for tag in content.tags]:
                factors.append(f"Interest: {interest}")
        
        # Value category
        if content.value_category in profile.value_preferences:
            factors.append(f"Category: {content.value_category.value}")
        
        # Skill matches
        for skill in profile.skill_levels:
            if skill.lower() in [tag.lower() for tag in content.tags]:
                factors.append(f"Skill: {skill}")
        
        return factors
    
    async def get_value_content(self, content_type: Optional[str] = None,
                              value_category: Optional[str] = None,
                              min_value_score: float = 0.0, limit: int = 50) -> List[ValueContent]:
        """Get value content with string-based filters"""
        
        # Convert string filters to enums
        content_type_enum = None
        if content_type:
            try:
                content_type_enum = ContentType(content_type)
            except ValueError:
                pass
        
        value_category_enum = None
        if value_category:
            try:
                value_category_enum = ValueCategory(value_category)
            except ValueError:
                pass
        
        return await self.fetch_value_content(content_type_enum, value_category_enum, min_value_score)[:limit]
    
    async def subscribe_to_value_feed(self, user_npub: str, content_type: Optional[str] = None,
                                    value_category: Optional[str] = None) -> Dict:
        """Subscribe user to value feed"""
        
        # Create or update user profile with subscription preferences
        if user_npub not in self.user_profiles:
            profile = UserValueProfile(
                user_npub=user_npub,
                interests=[],
                value_preferences={},
                skill_levels={},
                created_at=datetime.now().isoformat()
            )
            self.user_profiles[user_npub] = profile
        
        # Update preferences based on subscription
        if value_category:
            try:
                category_enum = ValueCategory(value_category)
                self.user_profiles[user_npub].value_preferences[category_enum] = 0.8
            except ValueError:
                pass
        
        return {
            "success": True,
            "message": f"Subscribed to value feed for {user_npub}",
            "subscription_details": {
                "content_type": content_type,
                "value_category": value_category
            }
        }
    
    async def get_feed_subscriptions(self) -> Dict:
        """Get all feed subscriptions"""
        subscriptions = {}
        
        for user_npub, profile in self.user_profiles.items():
            subscriptions[user_npub] = {
                "interests": profile.interests,
                "value_preferences": {cat.value: score for cat, score in profile.value_preferences.items()},
                "skill_levels": profile.skill_levels,
                "location": profile.location
            }
        
        return {
            "total_subscriptions": len(subscriptions),
            "subscriptions": subscriptions
        }
    
    async def get_value_streaming_analytics(self) -> Dict:
        """Get analytics for value streaming system"""
        total_content = len(self.content_database)
        total_users = len(self.user_profiles)
        total_matches = len(self.value_matches)
        
        # Calculate average value scores
        if total_content > 0:
            avg_value_score = sum(content.value_score for content in self.content_database) / total_content
        else:
            avg_value_score = 0.0
        
        # Calculate average match scores
        if total_matches > 0:
            avg_match_score = sum(match.match_score for match in self.value_matches) / total_matches
        else:
            avg_match_score = 0.0
        
        return {
            "total_content": total_content,
            "total_users": total_users,
            "total_matches": total_matches,
            "average_value_score": avg_value_score,
            "average_match_score": avg_match_score,
            "content_by_type": self._get_content_by_type(),
            "content_by_category": self._get_content_by_category()
        }
    
    def _get_content_by_type(self) -> Dict[str, int]:
        """Get content count by type"""
        counts = {}
        for content in self.content_database:
            content_type = content.content_type.value
            counts[content_type] = counts.get(content_type, 0) + 1
        return counts
    
    def _get_content_by_category(self) -> Dict[str, int]:
        """Get content count by category"""
        counts = {}
        for content in self.content_database:
            category = content.value_category.value
            counts[category] = counts.get(category, 0) + 1
        return counts 