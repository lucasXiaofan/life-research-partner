import { LearningSystemClient } from './client';

// Initialize the client
const client = new LearningSystemClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_ANON_KEY!
);

async function examples() {
  // Example 1: Add a learning resource
  const resource = await client.resources.create({
    title: 'Attention Is All You Need',
    source_url: 'https://arxiv.org/abs/1706.03762',
    content_text: 'The dominant sequence transduction models...',
    resource_type: 'paper',
    tags: ['transformers', 'attention', 'deep-learning']
  });
  console.log('Created resource:', resource.id);

  // Example 2: Capture an observation
  const observation = await client.observations.create({
    content: 'Multi-head attention shows 15% improvement over single head',
    experiment_id: 'exp-001',
    context: {
      model: 'transformer-base',
      dataset: 'WMT2014',
      metric: 'BLEU'
    }
  });
  console.log('Created observation:', observation.id);

  // Example 3: Create a takeaway linking observation and resource
  const takeaway = await client.takeaways.create({
    insight: 'Multi-head attention allows model to attend to different representation subspaces',
    assumption_before: 'Single attention mechanism is sufficient',
    assumption_after: 'Multiple attention heads capture different types of dependencies',
    observation_ids: [observation.id!],
    resource_ids: [resource.id!]
  });
  console.log('Created takeaway:', takeaway.id);

  // Example 4: Query resources by tags
  const mlPapers = await client.resources.getByTags(['deep-learning']);
  console.log('Found', mlPapers.length, 'deep learning resources');

  // Example 5: Get all observations for an experiment
  const expObservations = await client.observations.getByExperiment('exp-001');
  console.log('Found', expObservations.length, 'observations for exp-001');

  // Example 6: Get takeaway with all related data
  const fullTakeaway = await client.takeaways.getWithRelations(takeaway.id!);
  console.log('Takeaway with relations:', {
    insight: fullTakeaway.insight,
    observations: fullTakeaway.observations?.length,
    resources: fullTakeaway.resources?.length
  });
}

// Run examples
examples().catch(console.error);
