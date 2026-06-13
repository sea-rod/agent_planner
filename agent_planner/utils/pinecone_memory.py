from pinecone import Pinecone, CloudProvider, AwsRegion, EmbedModel, IndexEmbed
from datetime import datetime, timezone
import json
import os
import time
import structlog
from dotenv import load_dotenv

load_dotenv()

log = structlog.get_logger("atelier.memory")


class PineconeMemoryStore:
    def __init__(self):
        """Initialize Pinecone connection with integrated multilingual-e5-large embeddings."""
        t0 = time.perf_counter()
        try:
            self.client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
            elapsed_ms = (time.perf_counter() - t0) * 1000
            log.info("pinecone_connected", latency_ms=round(elapsed_ms, 2))
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
            log.error("pinecone_connect_failed", error=str(e), exc_info=True)
            raise

    def _get_rfc3339_timestamp(self):
        return datetime.now(timezone.utc).isoformat()

    def _create_indexes(self):
        """Create indexes with integrated embeddings if they don't exist."""
        try:
            existing_names = {idx["name"] for idx in self.client.list_indexes()}
            log.info("pinecone_indexes_listed", existing=list(existing_names))
        except Exception as e:
            log.error("pinecone_list_indexes_failed", error=str(e), exc_info=True)
            existing_names = set()

        # field_map points to the text field that gets embedded for each index
        indexes_to_create = {
            "user-preference": "preferenceText",
            "conversation-memory": "conversationText",
            "scheduling-pattern": "patternDescription",
        }

        for name, text_field in indexes_to_create.items():
            if name in existing_names:
                log.debug("pinecone_index_exists", index=name)
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
                log.info("pinecone_index_created", index=name)
            except Exception as e:
                log.error("pinecone_index_create_failed", index=name, error=str(e), exc_info=True)

    # ── Preferences ───────────────────────────────────────────────────────────

    def store_user_preference(
        self, user_id: str, preference_text: str, preference_type: str, preference_data: dict
    ):
        """Store user preference with automatic embedding."""
        t0 = time.perf_counter()

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
            log.info(
                "preference_stored",
                user_id=user_id,
                preference_type=preference_type,
                record_id=record["_id"],
                latency_ms=round((time.perf_counter() - t0) * 1000, 2),
            )
            return record["_id"]
        except Exception as e:
            log.error(
                "preference_store_failed",
                user_id=user_id,
                preference_type=preference_type,
                error=str(e),
                exc_info=True,
            )
            raise

    def get_relevant_preferences(self, user_id: str, query: str, limit: int = 5):
        """Retrieve semantically similar preferences."""
        t0 = time.perf_counter()

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
            log.error("preference_query_failed", user_id=user_id, error=str(e), exc_info=True)
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

        log.info(
            "preferences_retrieved",
            user_id=user_id,
            results_count=len(results),
            latency_ms=round((time.perf_counter() - t0) * 1000, 2),
        )
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
        t0 = time.perf_counter()

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
            log.info(
                "conversation_turn_stored",
                user_id=user_id,
                thread_id=thread_id,
                task_type=task_type,
                successful=successful,
                record_id=record["_id"],
                latency_ms=round((time.perf_counter() - t0) * 1000, 2),
            )
            return record["_id"]
        except Exception as e:
            log.error(
                "conversation_turn_store_failed",
                user_id=user_id,
                thread_id=thread_id,
                error=str(e),
                exc_info=True,
            )
            raise

    def retrieve_similar_conversations(
        self, user_id: str, current_context: str, limit: int = 3
    ):
        """Find semantically similar past conversations."""
        t0 = time.perf_counter()

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
            log.error("conversation_query_failed", user_id=user_id, error=str(e), exc_info=True)
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

        log.info(
            "conversations_retrieved",
            user_id=user_id,
            results_count=len(results),
            latency_ms=round((time.perf_counter() - t0) * 1000, 2),
        )
        return results

    # ── Scheduling patterns ───────────────────────────────────────────────────

    def store_scheduling_pattern(
        self, user_id: str, pattern_description: str, task_type: str, task_data: dict
    ):
        """Store scheduling pattern with embedding."""
        t0 = time.perf_counter()

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
            log.warning("scheduling_pattern_invalid_duration", raw_duration=duration, fallback=60)
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
            log.info(
                "scheduling_pattern_stored",
                user_id=user_id,
                task_type=task_type,
                duration=duration,
                record_id=record["_id"],
                latency_ms=round((time.perf_counter() - t0) * 1000, 2),
            )
            return record["_id"]
        except Exception as e:
            log.error(
                "scheduling_pattern_store_failed",
                user_id=user_id,
                task_type=task_type,
                error=str(e),
                exc_info=True,
            )
            raise

    def find_similar_patterns(
        self, user_id: str, task_description: str, limit: int = 5
    ):
        """Find similar past scheduling decisions."""
        t0 = time.perf_counter()

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
            log.error("pattern_query_failed", user_id=user_id, error=str(e), exc_info=True)
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

        log.info(
            "patterns_retrieved",
            user_id=user_id,
            results_count=len(results),
            latency_ms=round((time.perf_counter() - t0) * 1000, 2),
        )
        return results

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def close(self):
        # Pinecone's REST client doesn't hold a persistent connection that needs closing,
        # but kept for interface parity with the Weaviate version.
        log.info("pinecone_connection_closed")