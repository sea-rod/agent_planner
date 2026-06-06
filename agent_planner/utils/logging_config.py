"""
Atelier Logging Configuration
structlog-based structured JSON logging for Uvicorn + FastAPI + LangGraph.
"""

import logging
import sys
import time
import hashlib
from contextvars import ContextVar

import structlog

# ── Constants ────────────────────────────────────────────────────────────────

LOG_LEVEL = "INFO"
SLOW_REQUEST_THRESHOLD_MS = 2000

# Per-request context — bind once in middleware, available everywhere in that request
_request_ctx: ContextVar[dict] = ContextVar("request_ctx", default={})


# ── Setup: call once at app startup ─────────────────────────────────────────

def setup_logging(level: str = LOG_LEVEL, pretty: bool = False) -> None:
    """
    Configure structlog + stdlib logging.
    Call this once in main.py before anything else.

    Args:
        level:  Log level string ("DEBUG", "INFO", "WARNING", "ERROR")
        pretty: If True, use human-readable console output (local dev only).
                In production always leave False → JSON output.
    """
    shared_processors = [
        structlog.contextvars.merge_contextvars,          # picks up bind_contextvars() calls
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        _add_service_name,
    ]

    if pretty:
        # Dev: coloured, human-readable
        renderer = structlog.dev.ConsoleRenderer()
    else:
        # Production: strict JSON — one line per event, all fields top-level
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)

    # Silence noisy third-party loggers
    for noisy in ("httpx", "httpcore", "hpack"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def _add_service_name(logger, method, event_dict):
    event_dict.setdefault("service", "atelier")
    return event_dict


# ── Uvicorn log_config ───────────────────────────────────────────────────────
# Pass to uvicorn.run(log_config=UVICORN_LOG_CONFIG) so uvicorn's own
# access/error logs go through structlog instead of its default formatter.

UVICORN_LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "uvicorn":        {"handlers": ["default"], "level": "INFO",  "propagate": False},
        "uvicorn.error":  {"handlers": ["default"], "level": "INFO",  "propagate": False},
        "uvicorn.access": {"handlers": ["default"], "level": "INFO",  "propagate": False},
    },
}


# ── Domain Loggers ───────────────────────────────────────────────────────────
# Import these directly in each module — they're cheap to create.

auth_log     = structlog.get_logger("atelier.auth")
agent_log    = structlog.get_logger("atelier.agent")
calendar_log = structlog.get_logger("atelier.calendar")
db_log       = structlog.get_logger("atelier.db")
intent_log   = structlog.get_logger("atelier.intent")
http_log     = structlog.get_logger("atelier.http")


# ── Request Context Binding ──────────────────────────────────────────────────

def bind_request_context(user_id: str | None = None, request_id: str | None = None) -> None:
    """
    Bind per-request fields into structlog's context vars.
    Call at the top of RequestLoggingMiddleware — every log within the
    request will automatically carry user_id and request_id.
    """
    ctx: dict = {}
    if user_id:
        ctx["user_id"] = user_id
    if request_id:
        ctx["request_id"] = request_id
    structlog.contextvars.bind_contextvars(**ctx)


def clear_request_context() -> None:
    structlog.contextvars.clear_contextvars()


# ── Logging Helpers ──────────────────────────────────────────────────────────

def log_token_refresh(user_id: str, provider: str, success: bool, error: str | None = None) -> None:
    if success:
        auth_log.info("token_refresh_succeeded", user_id=user_id, provider=provider)
    else:
        auth_log.error("token_refresh_failed", user_id=user_id, provider=provider, error=error)


def log_oauth_callback(user_id: str, provider: str, scopes: list[str]) -> None:
    auth_log.info("oauth_callback_received", user_id=user_id, provider=provider, scopes=scopes)


def log_graph_node(node: str, elapsed_ms: float, status: str = "ok", error: str | None = None) -> None:
    if error:
        agent_log.error("graph_node_failed", node=node, elapsed_ms=round(elapsed_ms, 2), error=error)
    else:
        agent_log.info("graph_node_completed", node=node, elapsed_ms=round(elapsed_ms, 2), status=status)


def log_groq_call(model: str, prompt_tokens: int, completion_tokens: int, latency_ms: float) -> None:
    agent_log.info(
        "groq_api_call",
        model=model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        latency_ms=round(latency_ms, 2),
    )


def log_calendar_api(method: str, calendar_id: str, status_code: int, latency_ms: float) -> None:
    kwargs = dict(method=method, calendar_id=calendar_id, status_code=status_code, latency_ms=round(latency_ms, 2))
    if status_code == 429:
        calendar_log.warning("calendar_api_rate_limited", **kwargs)
    elif status_code >= 400:
        calendar_log.error("calendar_api_error", **kwargs)
    else:
        calendar_log.info("calendar_api_call", **kwargs)


def log_db_error(operation: str, table: str, error: str, rls_suspect: bool = False) -> None:
    db_log.error(
        "db_error",
        operation=operation,
        table=table,
        error=error,
        rls_suspect=rls_suspect,
    )


def log_intent(text: str, intent: str, confidence: float, threshold: float = 0.6) -> None:
    text_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
    kwargs = dict(text_hash=text_hash, intent=intent, confidence=round(confidence, 4))
    if confidence < threshold:
        intent_log.warning("intent_low_confidence", **kwargs)
    else:
        intent_log.info("intent_classified", **kwargs)


# ── FastAPI Middleware ────────────────────────────────────────────────────────

class RequestLoggingMiddleware:
    """
    ASGI middleware that:
    - Generates a request_id and binds it to structlog context
    - Logs every request with method, path, status, latency
    - Flags slow requests above SLOW_REQUEST_THRESHOLD_MS
    - Clears context after each request (critical for async safety)

    Usage in main.py:
        app.add_middleware(RequestLoggingMiddleware)
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        import uuid
        request_id = str(uuid.uuid4())[:8]
        method = scope.get("method", "")
        path = scope.get("path", "")
        status_code = 500
        start = time.perf_counter()

        # Bind request_id so all downstream logs carry it automatically
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
            kwargs = dict(method=method, path=path, status_code=status_code, elapsed_ms=elapsed_ms)

            if elapsed_ms > SLOW_REQUEST_THRESHOLD_MS:
                http_log.warning("http_request_slow", slow=True, **kwargs)
            elif status_code >= 500:
                http_log.error("http_request_error", **kwargs)
            elif status_code >= 400:
                http_log.warning("http_request_client_error", **kwargs)
            else:
                http_log.info("http_request", **kwargs)

            structlog.contextvars.clear_contextvars()