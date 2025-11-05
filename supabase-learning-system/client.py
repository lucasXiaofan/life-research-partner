"""
Supabase Learning System Client
A minimal learning system - like NotebookLM but self-managed
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from supabase import create_client, Client


@dataclass
class LearningResource:
    title: str
    resource_type: str  # 'paper' | 'blog' | 'documentation' | 'other'
    source_url: Optional[str] = None
    content_text: Optional[str] = None
    tags: Optional[List[str]] = None
    id: Optional[str] = None
    added_at: Optional[str] = None


@dataclass
class Observation:
    content: str
    experiment_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    id: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Takeaway:
    insight: str
    assumption_before: Optional[str] = None
    assumption_after: Optional[str] = None
    observation_ids: Optional[List[str]] = None
    resource_ids: Optional[List[str]] = None
    id: Optional[str] = None
    created_at: Optional[str] = None


class LearningResourcesAPI:
    """API for managing learning resources"""

    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.table = 'learning_resources'

    def create(self, resource: LearningResource) -> Dict[str, Any]:
        """Create a new learning resource"""
        data = {k: v for k, v in asdict(resource).items() if v is not None and k not in ['id', 'added_at']}
        response = self.supabase.table(self.table).insert(data).execute()
        return response.data[0]

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all learning resources"""
        response = self.supabase.table(self.table).select('*').order('added_at', desc=True).execute()
        return response.data

    def get_by_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        """Get resources that contain any of the specified tags"""
        response = self.supabase.table(self.table).select('*').contains('tags', tags).execute()
        return response.data

    def get_by_id(self, resource_id: str) -> Dict[str, Any]:
        """Get a specific resource by ID"""
        response = self.supabase.table(self.table).select('*').eq('id', resource_id).execute()
        return response.data[0] if response.data else None


class ObservationsAPI:
    """API for managing observations"""

    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.table = 'observations'

    def create(self, observation: Observation) -> Dict[str, Any]:
        """Create a new observation"""
        data = {k: v for k, v in asdict(observation).items() if v is not None and k not in ['id', 'created_at']}
        response = self.supabase.table(self.table).insert(data).execute()
        return response.data[0]

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all observations"""
        response = self.supabase.table(self.table).select('*').order('created_at', desc=True).execute()
        return response.data

    def get_by_experiment(self, experiment_id: str) -> List[Dict[str, Any]]:
        """Get all observations for a specific experiment"""
        response = self.supabase.table(self.table).select('*').eq('experiment_id', experiment_id).order('created_at', desc=True).execute()
        return response.data


class TakeawaysAPI:
    """API for managing takeaways"""

    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.table = 'takeaways'

    def create(self, takeaway: Takeaway) -> Dict[str, Any]:
        """Create a new takeaway"""
        data = {k: v for k, v in asdict(takeaway).items() if v is not None and k not in ['id', 'created_at']}
        response = self.supabase.table(self.table).insert(data).execute()
        return response.data[0]

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all takeaways"""
        response = self.supabase.table(self.table).select('*').order('created_at', desc=True).execute()
        return response.data

    def get_by_id(self, takeaway_id: str) -> Dict[str, Any]:
        """Get a specific takeaway by ID"""
        response = self.supabase.table(self.table).select('*').eq('id', takeaway_id).execute()
        return response.data[0] if response.data else None

    def get_with_relations(self, takeaway_id: str) -> Dict[str, Any]:
        """Get takeaway with all related observations and resources"""
        takeaway = self.get_by_id(takeaway_id)

        if not takeaway:
            return None

        # Fetch related observations
        if takeaway.get('observation_ids'):
            obs_response = self.supabase.table('observations').select('*').in_('id', takeaway['observation_ids']).execute()
            takeaway['observations'] = obs_response.data

        # Fetch related resources
        if takeaway.get('resource_ids'):
            res_response = self.supabase.table('learning_resources').select('*').in_('id', takeaway['resource_ids']).execute()
            takeaway['resources'] = res_response.data

        return takeaway


class LearningSystemClient:
    """Main client for the Supabase Learning System"""

    def __init__(self, supabase_url: str, supabase_key: str):
        """
        Initialize the learning system client

        Args:
            supabase_url: Your Supabase project URL
            supabase_key: Your Supabase anon/service key
        """
        self.supabase = create_client(supabase_url, supabase_key)
        self.resources = LearningResourcesAPI(self.supabase)
        self.observations = ObservationsAPI(self.supabase)
        self.takeaways = TakeawaysAPI(self.supabase)
