from agent_planner.utils.weaviate_memory import WeaviateMemoryStore

# Initialize memory store
memory = WeaviateMemoryStore()

# Test 1: Store a user preference
print("\n=== Test 1: Store User Preference ===")
memory.store_user_preference(
    user_id="user123",
    preference_text="I prefer to schedule meetings in the morning between 9 AM and 11 AM",
    preference_type="meeting_time",
    preference_data={"start_hour": 9, "end_hour": 11, "task_type": "meeting"}
)

# Test 2: Retrieve relevant preferences
print("\n=== Test 2: Retrieve Preferences ===")
preferences = memory.get_relevant_preferences(
    user_id="user123",
    query="When should I schedule a team sync?"
)
print(f"Found {len(preferences)} relevant preferences:")
for pref in preferences:
    print(f"  - {pref['text']}")

# Test 3: Store conversation
print("\n=== Test 3: Store Conversation ===")
memory.store_conversation_turn(
    user_id="user123",
    thread_id="thread_001",
    user_message="Schedule a team meeting for tomorrow at 10 AM",
    assistant_response="I've scheduled a team meeting for tomorrow at 10:00 AM",
    task_type="reminder",
    successful=True
)

# Test 4: Find similar conversations
print("\n=== Test 4: Find Similar Conversations ===")
similar = memory.retrieve_similar_conversations(
    user_id="user123",
    current_context="I need to organize a team discussion"
)
print(f"Found {len(similar)} similar conversations:")
for conv in similar:
    print(f"  - User: {conv['user_message'][:50]}...")

# Test 5: Store scheduling pattern
print("\n=== Test 5: Store Scheduling Pattern ===")
memory.store_scheduling_pattern(
    user_id="user123",
    pattern_description="Team meetings are usually scheduled on Monday mornings",
    task_type="meeting",
    task_data={
        "summary": "Team Sync",
        "start": "2025-11-04T10:00:00",
        "duration": 60,
        "day_pattern": "Monday"
    }
)

# Test 6: Find similar patterns
print("\n=== Test 6: Find Similar Patterns ===")
patterns = memory.find_similar_patterns(
    user_id="user123",
    task_description="weekly team standup"
)
print(f"Found {len(patterns)} similar patterns:")
for pattern in patterns:
    print(f"  - {pattern['description']}")

memory.close()
print("\n✓ All tests completed!")
