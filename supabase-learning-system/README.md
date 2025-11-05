# Supabase Learning System

A minimal learning system using Supabase - like NotebookLM but self-managed.

## Features

- **Learning Resources**: Store papers, blog posts, and documentation with full-text content
- **Observations**: Fast capture of experiment results and raw data
- **Takeaways**: Link insights to observations and resources, track belief changes

## Database Schema

### learning_resources
Store papers (PDF → text via docling), blog posts, documentation
- `id`: UUID primary key
- `title`: Resource title
- `source_url`: Original URL
- `content_text`: Full text content
- `resource_type`: paper | blog | documentation | other
- `tags`: Array of tags for categorization
- `added_at`: Timestamp

### observations
Fast capture without structure
- `id`: UUID primary key
- `content`: Observation text
- `experiment_id`: Link to experiment
- `context`: JSONB for flexible metadata
- `created_at`: Timestamp

### takeaways
Link raw data → learning, track belief changes
- `id`: UUID primary key
- `insight`: Key insight learned
- `assumption_before`: What you believed before
- `assumption_after`: What you believe now
- `observation_ids`: Array of related observation UUIDs
- `resource_ids`: Array of related resource UUIDs
- `created_at`: Timestamp

## Setup

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Get your project URL and anon key from Settings → API

### 2. Run Migrations

In your Supabase project dashboard:
1. Go to SQL Editor
2. Copy and paste the contents of `migrations/001_create_tables.sql`
3. Run the migration

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

### 4. Install Dependencies

```bash
npm install
```

## Usage

```typescript
import { LearningSystemClient } from './src/client';

const client = new LearningSystemClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_ANON_KEY!
);

// Add a learning resource
const resource = await client.resources.create({
  title: 'Attention Is All You Need',
  source_url: 'https://arxiv.org/abs/1706.03762',
  content_text: 'The dominant sequence transduction models...',
  resource_type: 'paper',
  tags: ['transformers', 'attention']
});

// Capture an observation
const observation = await client.observations.create({
  content: 'Multi-head attention shows 15% improvement',
  experiment_id: 'exp-001',
  context: { model: 'transformer-base', metric: 'BLEU' }
});

// Create a takeaway
const takeaway = await client.takeaways.create({
  insight: 'Multiple attention heads capture different dependencies',
  assumption_before: 'Single attention is sufficient',
  assumption_after: 'Multiple heads improve representation',
  observation_ids: [observation.id],
  resource_ids: [resource.id]
});
```

## Run Example

```bash
npm run example
```

## API Methods

### Resources
- `create(resource)` - Add a new resource
- `getAll()` - Get all resources
- `getByTags(tags[])` - Filter by tags
- `getById(id)` - Get specific resource

### Observations
- `create(observation)` - Capture observation
- `getAll()` - Get all observations
- `getByExperiment(experimentId)` - Filter by experiment

### Takeaways
- `create(takeaway)` - Create insight
- `getAll()` - Get all takeaways
- `getById(id)` - Get specific takeaway
- `getWithRelations(id)` - Get with linked observations & resources

## Next Steps

- Integrate PDF processing with docling
- Add full-text search
- Build a simple UI
- Add embedding generation for semantic search
