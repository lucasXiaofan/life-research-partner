import { createClient, SupabaseClient } from '@supabase/supabase-js';

// Types
export interface LearningResource {
  id?: string;
  title: string;
  source_url?: string;
  content_text?: string;
  resource_type: 'paper' | 'blog' | 'documentation' | 'other';
  tags?: string[];
  added_at?: string;
}

export interface Observation {
  id?: string;
  content: string;
  experiment_id?: string;
  context?: Record<string, any>;
  created_at?: string;
}

export interface Takeaway {
  id?: string;
  insight: string;
  assumption_before?: string;
  assumption_after?: string;
  observation_ids?: string[];
  resource_ids?: string[];
  created_at?: string;
}

// Initialize Supabase client
export function initSupabase(url: string, anonKey: string): SupabaseClient {
  return createClient(url, anonKey);
}

// Learning Resources API
export class LearningResourcesAPI {
  constructor(private supabase: SupabaseClient) {}

  async create(resource: LearningResource) {
    const { data, error } = await this.supabase
      .from('learning_resources')
      .insert(resource)
      .select()
      .single();

    if (error) throw error;
    return data;
  }

  async getAll() {
    const { data, error } = await this.supabase
      .from('learning_resources')
      .select('*')
      .order('added_at', { ascending: false });

    if (error) throw error;
    return data;
  }

  async getByTags(tags: string[]) {
    const { data, error } = await this.supabase
      .from('learning_resources')
      .select('*')
      .contains('tags', tags);

    if (error) throw error;
    return data;
  }

  async getById(id: string) {
    const { data, error } = await this.supabase
      .from('learning_resources')
      .select('*')
      .eq('id', id)
      .single();

    if (error) throw error;
    return data;
  }
}

// Observations API
export class ObservationsAPI {
  constructor(private supabase: SupabaseClient) {}

  async create(observation: Observation) {
    const { data, error } = await this.supabase
      .from('observations')
      .insert(observation)
      .select()
      .single();

    if (error) throw error;
    return data;
  }

  async getAll() {
    const { data, error } = await this.supabase
      .from('observations')
      .select('*')
      .order('created_at', { ascending: false });

    if (error) throw error;
    return data;
  }

  async getByExperiment(experimentId: string) {
    const { data, error } = await this.supabase
      .from('observations')
      .select('*')
      .eq('experiment_id', experimentId)
      .order('created_at', { ascending: false });

    if (error) throw error;
    return data;
  }
}

// Takeaways API
export class TakeawaysAPI {
  constructor(private supabase: SupabaseClient) {}

  async create(takeaway: Takeaway) {
    const { data, error } = await this.supabase
      .from('takeaways')
      .insert(takeaway)
      .select()
      .single();

    if (error) throw error;
    return data;
  }

  async getAll() {
    const { data, error } = await this.supabase
      .from('takeaways')
      .select('*')
      .order('created_at', { ascending: false });

    if (error) throw error;
    return data;
  }

  async getById(id: string) {
    const { data, error } = await this.supabase
      .from('takeaways')
      .select('*')
      .eq('id', id)
      .single();

    if (error) throw error;
    return data;
  }

  // Get takeaway with related observations and resources
  async getWithRelations(id: string) {
    const takeaway = await this.getById(id);

    if (takeaway.observation_ids?.length) {
      const { data: observations } = await this.supabase
        .from('observations')
        .select('*')
        .in('id', takeaway.observation_ids);
      takeaway.observations = observations;
    }

    if (takeaway.resource_ids?.length) {
      const { data: resources } = await this.supabase
        .from('learning_resources')
        .select('*')
        .in('id', takeaway.resource_ids);
      takeaway.resources = resources;
    }

    return takeaway;
  }
}

// Main client
export class LearningSystemClient {
  public resources: LearningResourcesAPI;
  public observations: ObservationsAPI;
  public takeaways: TakeawaysAPI;

  constructor(supabaseUrl: string, supabaseKey: string) {
    const supabase = initSupabase(supabaseUrl, supabaseKey);
    this.resources = new LearningResourcesAPI(supabase);
    this.observations = new ObservationsAPI(supabase);
    this.takeaways = new TakeawaysAPI(supabase);
  }
}
