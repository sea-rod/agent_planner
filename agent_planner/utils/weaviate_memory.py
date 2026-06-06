import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import Filter
from datetime import datetime, timezone
import json
import os
import time
import structlog
from dotenv import load_dotenv

load_dotenv()

log = structlog.get_logger("atelier.memory")


class WeaviateMemoryStore:
    def __init__(self):
        """Initialize Weaviate Cloud connection with free Cohere embeddings."""
        t0 = time.perf_counter()
        try:
            self.client = weaviate.connect_to_weaviate_cloud(
                cluster_url=os.getenv("WEAVIATE_URL"),
                auth_credentials=Auth.api_key(os.getenv("WEAVIATE_API_KEY")),
                headers={"X-Cohere-Api-Key": os.getenv("COHERE_API_KEY")},
            )
            elapsed_ms = (time.perf_counter() - t0) * 1000
            log.info("weaviate_connected", ready=self.client.is_ready(), latency_ms=round(elapsed_ms, 2))
            self._create_collections()
        except Exception as e:
            log.error("weaviate_connect_failed", error=str(e), exc_info=True)
            raise

    def _get_rfc3339_timestamp(self):
        return datetime.now(timezone.utc).isoformat()

    def _create_collections(self):
        """Create collections with Cohere embeddings if they don't exist."""
        try:
            existing = self.client.collections.list_all(simple=True)
            existing_names = list(existing.keys()) if isinstance(existing, dict) else []
            log.info("weaviate_collections_listed", existing=existing_names)
        except Exception as e:
            log.error("weaviate_list_collections_failed", error=str(e), exc_info=True)
            existing_names = []

        collections_to_create = {
            "UserPreference": {
                "description": "User scheduling preferences and patterns",
                "properties": [
                    Property(name="userId",         data_type=DataType.TEXT),
                    Property(name="preferenceText", data_type=DataType.TEXT),
                    Property(name="preferenceType", data_type=DataType.TEXT),
                    Property(name="preferenceData", data_type=DataType.TEXT),
                    Property(name="timestamp",      data_type=DataType.DATE),
                ],
            },
            "ConversationMemory": {
                "description": "Semantic conversation history",
                "properties": [
                    Property(name="userId",            data_type=DataType.TEXT),
                    Property(name="threadId",          data_type=DataType.TEXT),
                    Property(name="conversationText",  data_type=DataType.TEXT),
                    Property(name="userMessage",       data_type=DataType.TEXT),
                    Property(name="assistantMessage",  data_type=DataType.TEXT),
                    Property(name="taskType",          data_type=DataType.TEXT),
                    Property(name="successful",        data_type=DataType.BOOL),
                    Property(name="timestamp",         data_type=DataType.DATE),
                ],
            },
            "SchedulingPattern": {
                "description": "Learned scheduling patterns",
                "properties": [
                    Property(name="userId",              data_type=DataType.TEXT),
                    Property(name="patternDescription",  data_type=DataType.TEXT),
                    Property(name="taskType",            data_type=DataType.TEXT),
                    Property(name="taskSummary",         data_type=DataType.TEXT),
                    Property(name="preferredTime",       data_type=DataType.TEXT),
                    Property(name="duration",            data_type=DataType.INT),
                    Property(name="dayPattern",          data_type=DataType.TEXT),
                    Property(name="frequency",           data_type=DataType.INT),
                    Property(name="timestamp",           data_type=DataType.DATE),
                ],
            },
        }

        for name, config in collections_to_create.items():
            if name in existing_names:
                log.debug("weaviate_collection_exists", collection=name)
                continue
            try:
                self.client.collections.create(
                    name=name,
                    description=config["description"],
                    vectorizer_config=Configure.Vectorizer.text2vec_cohere(model="embed-english-v3.0"),
                    vector_index_config=Configure.VectorIndex.flat(),
                    properties=config["properties"],
                )
                log.info("weaviate_collection_created", collection=name)
            except Exception as e:
                log.error("weaviate_collection_create_failed", collection=name, error=str(e), exc_info=True)

    # ── Preferences ───────────────────────────────────────────────────────────

    def store_user_preference(
        self, user_id: str, preference_text: str, preference_type: str, preference_data: dict
    ):
        """Store user preference with automatic embedding."""
        t0 = time.perf_counter()
        collection = self.client.collections.get("UserPreference")

        data_object = {
            "userId":         user_id,
            "preferenceText": preference_text,
            "preferenceType": preference_type,
            "preferenceData": json.dumps(preference_data),
            "timestamp":      self._get_rfc3339_timestamp(),
        }

        try:
            uuid = collection.data.insert(data_object)
            log.info(
                "preference_stored",
                user_id=user_id,
                preference_type=preference_type,
                uuid=str(uuid),
                latency_ms=round((time.perf_counter() - t0) * 1000, 2),
            )
            return uuid
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
        collection = self.client.collections.get("UserPreference")

        try:
            response = collection.query.near_text(
                query=query,
                limit=limit,
                filters=Filter.by_property("userId").equal(user_id),
            )
        except Exception as e:
            log.error("preference_query_failed", user_id=user_id, error=str(e), exc_info=True)
            raise

        results = [
            {
                "text":      obj.properties["preferenceText"],
                "type":      obj.properties["preferenceType"],
                "data":      json.loads(obj.properties["preferenceData"]),
                "timestamp": obj.properties["timestamp"],
            }
            for obj in response.objects
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
        collection = self.client.collections.get("ConversationMemory")

        conversation_text = (
            f"User asked: {user_message}\n"
            f"Assistant responded: {assistant_response}\n"
            f"Task was: {task_type}"
        )

        data_object = {
            "userId":           user_id,
            "threadId":         thread_id,
            "conversationText": conversation_text,
            "userMessage":      user_message,
            "assistantMessage": assistant_response,
            "taskType":         task_type,
            "successful":       successful,
            "timestamp":        self._get_rfc3339_timestamp(),
        }

        try:
            uuid = collection.data.insert(data_object)
            log.info(
                "conversation_turn_stored",
                user_id=user_id,
                thread_id=thread_id,
                task_type=task_type,
                successful=successful,
                uuid=str(uuid),
                latency_ms=round((time.perf_counter() - t0) * 1000, 2),
            )
            return uuid
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
        collection = self.client.collections.get("ConversationMemory")

        try:
            response = collection.query.near_text(
                query=current_context,
                limit=limit,
                filters=Filter.by_property("userId").equal(user_id),
            )
        except Exception as e:
            log.error("conversation_query_failed", user_id=user_id, error=str(e), exc_info=True)
            raise

        results = [
            {
                "user_message":      obj.properties["userMessage"],
                "assistant_message": obj.properties["assistantMessage"],
                "task_type":         obj.properties["taskType"],
                "timestamp":         obj.properties["timestamp"],
            }
            for obj in response.objects
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
        collection = self.client.collections.get("SchedulingPattern")

        preferred_time = task_data.get("start", "")
        if isinstance(preferred_time, dict):
            preferred_time = preferred_time.get("dateTime", str(preferred_time))
        preferred_time = str(preferred_time) if preferred_time else ""

        task_summary = str(task_data.get("summary", "") or "")
        day_pattern  = str(task_data.get("day_pattern", "weekday") or "weekday")

        duration = task_data.get("duration", 60)
        try:
            duration = int(duration)
        except (ValueError, TypeError):
            log.warning("scheduling_pattern_invalid_duration", raw_duration=duration, fallback=60)
            duration = 60

        data_object = {
            "userId":             user_id,
            "patternDescription": pattern_description,
            "taskType":           task_type,
            "taskSummary":        task_summary,
            "preferredTime":      preferred_time,
            "duration":           duration,
            "dayPattern":         day_pattern,
            "frequency":          1,
            "timestamp":          self._get_rfc3339_timestamp(),
        }

        try:
            uuid = collection.data.insert(data_object)
            log.info(
                "scheduling_pattern_stored",
                user_id=user_id,
                task_type=task_type,
                duration=duration,
                uuid=str(uuid),
                latency_ms=round((time.perf_counter() - t0) * 1000, 2),
            )
            return uuid
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
        collection = self.client.collections.get("SchedulingPattern")

        try:
            response = collection.query.near_text(
                query=task_description,
                limit=limit,
                filters=Filter.by_property("userId").equal(user_id),
            )
        except Exception as e:
            log.error("pattern_query_failed", user_id=user_id, error=str(e), exc_info=True)
            raise

        results = [
            {
                "description":   obj.properties["patternDescription"],
                "task_type":     obj.properties["taskType"],
                "preferred_time": obj.properties["preferredTime"],
                "duration":      obj.properties["duration"],
                "day_pattern":   obj.properties["dayPattern"],
            }
            for obj in response.objects
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
        self.client.close()
        log.info("weaviate_connection_closed")