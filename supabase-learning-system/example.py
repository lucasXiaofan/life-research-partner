"""
Example usage of the Supabase Learning System
"""

import os
from client import LearningSystemClient, LearningResource, Observation, Takeaway


def main():
    # Initialize the client
    client = LearningSystemClient(
        supabase_url=os.getenv('SUPABASE_URL'),
        supabase_key=os.getenv('SUPABASE_ANON_KEY')
    )

    print("=== Supabase Learning System Examples ===\n")

    # Example 1: Add a learning resource
    print("1. Creating a learning resource...")
    resource = client.resources.create(LearningResource(
        title='Attention Is All You Need',
        source_url='https://arxiv.org/abs/1706.03762',
        content_text='The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...',
        resource_type='paper',
        tags=['transformers', 'attention', 'deep-learning']
    ))
    print(f"   Created resource: {resource['id']}")
    print(f"   Title: {resource['title']}\n")

    # Example 2: Capture an observation
    print("2. Creating an observation...")
    observation = client.observations.create(Observation(
        content='Multi-head attention shows 15% improvement over single head',
        experiment_id='exp-001',
        context={
            'model': 'transformer-base',
            'dataset': 'WMT2014',
            'metric': 'BLEU',
            'score': 28.4
        }
    ))
    print(f"   Created observation: {observation['id']}")
    print(f"   Content: {observation['content']}\n")

    # Example 3: Create a takeaway linking observation and resource
    print("3. Creating a takeaway...")
    takeaway = client.takeaways.create(Takeaway(
        insight='Multi-head attention allows model to attend to different representation subspaces',
        assumption_before='Single attention mechanism is sufficient for capturing dependencies',
        assumption_after='Multiple attention heads capture different types of dependencies simultaneously',
        observation_ids=[observation['id']],
        resource_ids=[resource['id']]
    ))
    print(f"   Created takeaway: {takeaway['id']}")
    print(f"   Insight: {takeaway['insight']}\n")

    # Example 4: Query resources by tags
    print("4. Querying resources by tags...")
    ml_papers = client.resources.get_by_tags(['deep-learning'])
    print(f"   Found {len(ml_papers)} deep learning resources\n")

    # Example 5: Get all observations for an experiment
    print("5. Getting observations for experiment...")
    exp_observations = client.observations.get_by_experiment('exp-001')
    print(f"   Found {len(exp_observations)} observations for exp-001\n")

    # Example 6: Get takeaway with all related data
    print("6. Getting takeaway with relations...")
    full_takeaway = client.takeaways.get_with_relations(takeaway['id'])
    print(f"   Insight: {full_takeaway['insight']}")
    print(f"   Linked observations: {len(full_takeaway.get('observations', []))}")
    print(f"   Linked resources: {len(full_takeaway.get('resources', []))}")

    print("\n=== All examples completed! ===")


if __name__ == '__main__':
    main()
