from pinecone import Pinecone, CloudProvider, AwsRegion, EmbedModel, IndexEmbed
from datetime import datetime, timezone
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()


class PineconeMemoryStore:
    def __init__(self):
        """Initialize Pinecone connection with integrated multilingual-e5-large embeddings."""
        try:
            self.client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
            self._create_indexes()

            self.preference_index = self.client.Index(
                host=self.client.describe_index("user-preference").host
            )
            self.conversation_index = self.client.Index(
                host=self.client.describe_index("conversation-memory").host
            )
            self.pattern_index = self.client.Index(
                host=self.client.describe_index("scheduling-pattern").host
            )
        except Exception as e:
            raise

    def _get_rfc3339_timestamp(self):
        return datetime.now(timezone.utc).isoformat()

    def _create_indexes(self):
        """Create indexes with integrated embeddings if they don't exist."""
        try:
            existing_names = {idx["name"] for idx in self.client.list_indexes()}
        except Exception as e:
            existing_names = set()

        # field_map points to the text field that gets embedded for each index
        indexes_to_create = {
            "user-preference": "preferenceText",
            "conversation-memory": "conversationText",
            "scheduling-pattern": "patternDescription",
        }

        for name, text_field in indexes_to_create.items():
            if name in existing_names:
                continue
            try:
                self.client.create_index_for_model(
                    name=name,
                    cloud=CloudProvider.AWS,
                    region=AwsRegion.US_EAST_1,
                    embed=IndexEmbed(
                        model=EmbedModel.Multilingual_E5_Large,
                        field_map={"text": text_field},
                    ),
                )
            except Exception as e:
                pass

    # ── Preferences ───────────────────────────────────────────────────────────

    def store_user_preference(
        self, user_id: str, preference_text: str, preference_type: str, preference_data: dict
    ):
        """Store user preference with automatic embedding."""
        record = {
            "_id": f"pref_{user_id}_{int(time.time() * 1000)}",
            "preferenceText": preference_text,
            "userId": user_id,
            "preferenceType": preference_type,
            "preferenceData": json.dumps(preference_data),
            "timestamp": self._get_rfc3339_timestamp(),
        }

        try:
            self.preference_index.upsert_records(
                namespace="default",
                records=[record],
            )
            print(f"Method store_user_preference returned: {record['_id']}")
            return record["_id"]
        except Exception as e:
            raise

    def get_relevant_preferences(self, user_id: str, query: str, limit: int = 5):
        """Retrieve semantically similar preferences."""
        try:
            response = self.preference_index.search(
                namespace="default",
                query={
                    "inputs": {"text": query},
                    "top_k": limit,
                    "filter": {"userId": {"$eq": user_id}},
                },
                fields=["preferenceText", "preferenceType", "preferenceData", "timestamp"],
            )
        except Exception as e:
            raise

        results = [
            {
                "text": hit["fields"]["preferenceText"],
                "type": hit["fields"]["preferenceType"],
                "data": json.loads(hit["fields"]["preferenceData"]),
                "timestamp": hit["fields"]["timestamp"],
            }
            for hit in response["result"]["hits"]
        ]

        print(f"Method get_relevant_preferences returned: {results}")
        return results

    # ── Conversation memory ───────────────────────────────────────────────────

    def store_conversation_turn(
        self,
        user_id: str,
        thread_id: str,
        user_message: str,
        assistant_response: str,
        task_type: str,
        successful: bool = True,
    ):
        """Store conversation with semantic embedding."""
        conversation_text = (
            f"User asked: {user_message}\n"
            f"Assistant responded: {assistant_response}\n"
            f"Task was: {task_type}"
        )

        record = {
            "_id": f"conv_{user_id}_{int(time.time() * 1000)}",
            "conversationText": conversation_text,
            "userId": user_id,
            "threadId": thread_id,
            "userMessage": user_message,
            "assistantMessage": assistant_response,
            "taskType": task_type,
            "successful": successful,
            "timestamp": self._get_rfc3339_timestamp(),
        }

        try:
            self.conversation_index.upsert_records(
                namespace="default",
                records=[record],
            )
            print(f"Method store_conversation_turn returned: {record['_id']}")
            return record["_id"]
        except Exception as e:
            raise

    def retrieve_similar_conversations(
        self, user_id: str, current_context: str, limit: int = 3
    ):
        """Find semantically similar past conversations."""
        try:
            response = self.conversation_index.search(
                namespace="default",
                query={
                    "inputs": {"text": current_context},
                    "top_k": limit,
                    "filter": {"userId": {"$eq": user_id}},
                },
                fields=["userMessage", "assistantMessage", "taskType", "timestamp"],
            )
        except Exception as e:
            raise

        results = [
            {
                "user_message": hit["fields"]["userMessage"],
                "assistant_message": hit["fields"]["assistantMessage"],
                "task_type": hit["fields"]["taskType"],
                "timestamp": hit["fields"]["timestamp"],
            }
            for hit in response["result"]["hits"]
        ]

        print(f"Method retrieve_similar_conversations returned: {results}")
        return results

    # ── Scheduling patterns ───────────────────────────────────────────────────

    def store_scheduling_pattern(
        self, user_id: str, pattern_description: str, task_type: str, task_data: dict
    ):
        """Store scheduling pattern with embedding."""
        preferred_time = task_data.get("start", "")
        if isinstance(preferred_time, dict):
            preferred_time = preferred_time.get("dateTime", str(preferred_time))
        preferred_time = str(preferred_time) if preferred_time else ""

        task_summary = str(task_data.get("summary", "") or "")
        day_pattern = str(task_data.get("day_pattern", "weekday") or "weekday")

        duration = task_data.get("duration", 60)
        try:
            duration = int(duration)
        except (ValueError, TypeError):
            duration = 60

        record = {
            "_id": f"pattern_{user_id}_{int(time.time() * 1000)}",
            "patternDescription": pattern_description,
            "userId": user_id,
            "taskType": task_type,
            "taskSummary": task_summary,
            "preferredTime": preferred_time,
            "duration": duration,
            "dayPattern": day_pattern,
            "frequency": 1,
            "timestamp": self._get_rfc3339_timestamp(),
        }

        try:
            self.pattern_index.upsert_records(
                namespace="default",
                records=[record],
            )
            print(f"Method store_scheduling_pattern returned: {record['_id']}")
            return record["_id"]
        except Exception as e:
            raise

    def find_similar_patterns(
        self, user_id: str, task_description: str, limit: int = 5
    ):
        """Find similar past scheduling decisions."""
        try:
            response = self.pattern_index.search(
                namespace="default",
                query={
                    "inputs": {"text": task_description},
                    "top_k": limit,
                    "filter": {"userId": {"$eq": user_id}},
                },
                fields=["patternDescription", "taskType", "preferredTime", "duration", "dayPattern"],
            )
        except Exception as e:
            raise

        results = [
            {
                "description": hit["fields"]["patternDescription"],
                "task_type": hit["fields"]["taskType"],
                "preferred_time": hit["fields"]["preferredTime"],
                "duration": hit["fields"]["duration"],
                "day_pattern": hit["fields"]["dayPattern"],
            }
            for hit in response["result"]["hits"]
        ]

        print(f"Method find_similar_patterns returned: {results}")
        return results

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def close(self):
        # Pinecone's REST client doesn't hold a persistent connection that needs closing,
        # but kept for interface parity with the Weaviate version.
        print("Method close called")