-- Create learning_resources table
CREATE TABLE learning_resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    source_url TEXT,
    content_text TEXT,
    resource_type TEXT NOT NULL CHECK (resource_type IN ('paper', 'blog', 'documentation', 'other')),
    tags TEXT[] DEFAULT '{}',
    added_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create observations table
CREATE TABLE observations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    experiment_id TEXT,
    context JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create takeaways table
CREATE TABLE takeaways (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    insight TEXT NOT NULL,
    assumption_before TEXT,
    assumption_after TEXT,
    observation_ids UUID[] DEFAULT '{}',
    resource_ids UUID[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX idx_learning_resources_tags ON learning_resources USING GIN(tags);
CREATE INDEX idx_learning_resources_type ON learning_resources(resource_type);
CREATE INDEX idx_observations_experiment ON observations(experiment_id);
CREATE INDEX idx_observations_created ON observations(created_at DESC);
CREATE INDEX idx_takeaways_created ON takeaways(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE learning_resources ENABLE ROW LEVEL SECURITY;
ALTER TABLE observations ENABLE ROW LEVEL SECURITY;
ALTER TABLE takeaways ENABLE ROW LEVEL SECURITY;

-- Create policies (allowing authenticated users full access for now)
CREATE POLICY "Enable all access for authenticated users" ON learning_resources
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Enable all access for authenticated users" ON observations
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Enable all access for authenticated users" ON takeaways
    FOR ALL USING (auth.role() = 'authenticated');
