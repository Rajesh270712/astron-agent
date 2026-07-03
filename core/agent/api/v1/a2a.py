"""A2A discovery adapter for the core agent service."""

import os
import uuid
from datetime import datetime, timezone
from typing import Annotated, TypeAlias

from fastapi import APIRouter, Header, HTTPException, Query

from agent.api.schemas.a2a import (
    A2AAgentCapabilities,
    A2AAgentCard,
    A2AAgentInterface,
    A2AAgentProvider,
    A2AAgentSkill,
    A2AAPIKeySecurityScheme,
    A2AAuthentication,
    A2AMessage,
    A2APart,
    A2ASecurityRequirement,
    A2ASecurityScheme,
    A2AStringList,
    A2ATask,
    A2ATaskArtifactUpdateEvent,
    A2ATaskEvents,
    A2ATaskList,
    A2ATaskSendParams,
    A2ATaskStatus,
    A2ATaskStatusUpdateEvent,
)

A2A_PROTOCOL_VERSION = "0.3.0"
ASTRON_AGENT_VERSION = "1.0.9"
_TERMINAL_TASK_STATES = {
    "TASK_STATE_COMPLETED",
    "TASK_STATE_FAILED",
    "TASK_STATE_CANCELED",
    "TASK_STATE_REJECTED",
}
_TaskEvent: TypeAlias = A2ATaskStatusUpdateEvent | A2ATaskArtifactUpdateEvent
_TASKS: dict[str, A2ATask] = {}
_TASK_EVENTS: dict[str, list[_TaskEvent]] = {}

a2a_discovery_router = APIRouter()
a2a_router = APIRouter(prefix="/a2a")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _public_base_url() -> str:
    configured_url = (
        os.getenv("A2A_PUBLIC_BASE_URL")
        or os.getenv("AGENT_BASE_URL")
        or f"http://localhost:{os.getenv('SERVICE_PORT', '8700')}"
    )
    return configured_url.rstrip("/")


def _agent_version() -> str:
    return os.getenv("ASTRON_AGENT_VERSION", ASTRON_AGENT_VERSION).removeprefix("v")


def build_agent_card() -> A2AAgentCard:
    """Build public A2A discovery metadata for the core agent service."""

    interface_url = f"{_public_base_url()}/agent/v1/a2a"
    return A2AAgentCard(
        protocolVersion=A2A_PROTOCOL_VERSION,
        name="Astron Agent",
        description="Astron Agent core runtime exposed through an A2A text adapter.",
        url=interface_url,
        preferredTransport="HTTP+JSON",
        supportedInterfaces=[
            A2AAgentInterface(
                url=interface_url,
                protocolBinding="HTTP+JSON",
                protocolVersion=A2A_PROTOCOL_VERSION,
            )
        ],
        provider=A2AAgentProvider(
            organization="iFLYTEK",
            url="https://github.com/iflytek/astron-agent",
        ),
        version=_agent_version(),
        capabilities=A2AAgentCapabilities(
            streaming=False,
            pushNotifications=False,
            extendedAgentCard=False,
        ),
        authentication=A2AAuthentication(
            schemes=["ApiKey"],
            credentials="x-consumer-username header",
        ),
        securitySchemes={
            "astronConsumer": A2ASecurityScheme(
                apiKeySecurityScheme=A2AAPIKeySecurityScheme(
                    description="Astron gateway consumer header.",
                    location="header",
                    name="x-consumer-username",
                )
            )
        },
        securityRequirements=[
            A2ASecurityRequirement(schemes={"astronConsumer": A2AStringList(list=[])})
        ],
        defaultInputModes=["text/plain"],
        defaultOutputModes=["text/plain"],
        skills=[
            A2AAgentSkill(
                id="astron-agent-chat",
                name="Astron Agent Chat",
                description="Send text to the configured Astron Agent runtime.",
                tags=["agent", "chat", "astron"],
                examples=["Summarize this workflow result."],
                inputModes=["text/plain"],
                outputModes=["text/plain"],
            )
        ],
    )


@a2a_discovery_router.get(  # type: ignore[misc]
    "/.well-known/agent-card.json",
    response_model=A2AAgentCard,
)
async def get_well_known_agent_card() -> A2AAgentCard:
    """Return the public A2A discovery card."""

    return build_agent_card()


@a2a_router.get(  # type: ignore[misc]
    "/agent-card.json",
    response_model=A2AAgentCard,
)
async def get_agent_card() -> A2AAgentCard:
    """Return the public A2A discovery card from the versioned API path."""

    return build_agent_card()


def _history_message(
    message: A2AMessage,
    task_id: str,
    context_id: str,
) -> A2AMessage:
    return message.model_copy(
        update={
            "task_id": task_id,
            "context_id": context_id,
            "role": "ROLE_USER",
        }
    )


def _status_message(task_id: str, context_id: str, text: str) -> A2AMessage:
    return A2AMessage(
        messageId=str(uuid.uuid4()),
        contextId=context_id,
        taskId=task_id,
        role="ROLE_AGENT",
        parts=[A2APart(text=text, mediaType="text/plain")],
    )


def _submitted_task_from_params(params: A2ATaskSendParams) -> A2ATask:
    task_id = params.id or params.message.task_id or str(uuid.uuid4())
    context_id = (
        params.context_id
        or params.session_id
        or params.message.context_id
        or str(uuid.uuid4())
    )
    return A2ATask(
        id=task_id,
        contextId=context_id,
        status=A2ATaskStatus(
            state="TASK_STATE_SUBMITTED",
            message=_status_message(
                task_id,
                context_id,
                "A2A task submitted to Astron Agent.",
            ),
            timestamp=_utc_now(),
        ),
        history=[
            _history_message(
                params.message,
                task_id=task_id,
                context_id=context_id,
            )
        ],
        metadata={
            "source": "astron-agent-core",
            "tenant": params.tenant,
        },
    )


def _record_task(task: A2ATask) -> None:
    """Store task state and the latest task runtime events in process memory."""

    _TASKS[task.id] = task
    final = task.status.state in _TERMINAL_TASK_STATES
    events: list[_TaskEvent] = [
        A2ATaskStatusUpdateEvent(
            taskId=task.id,
            contextId=task.context_id,
            status=task.status,
            final=final,
        )
    ]
    events.extend(
        A2ATaskArtifactUpdateEvent(
            taskId=task.id,
            contextId=task.context_id,
            artifact=artifact,
            append=False,
            lastChunk=True,
        )
        for artifact in task.artifacts
    )
    _TASK_EVENTS[task.id] = events


@a2a_router.post(  # type: ignore[misc]
    "/tasks:send",
    response_model=A2ATask,
)
async def send_task(
    x_consumer_username: Annotated[str, Header()],
    params: A2ATaskSendParams,
) -> A2ATask:
    """Record a task-oriented A2A request in the core agent runtime store."""

    task = _submitted_task_from_params(
        params.model_copy(
            update={
                "tenant": params.tenant or x_consumer_username,
            }
        )
    )
    _record_task(task)
    return task


@a2a_router.get(  # type: ignore[misc]
    "/tasks",
    response_model=A2ATaskList,
)
async def list_tasks(
    x_consumer_username: Annotated[str, Header()],
) -> A2ATaskList:
    """Return recorded task runtime states."""

    return A2ATaskList(tasks=list(_TASKS.values()))


@a2a_router.get(  # type: ignore[misc]
    "/tasks/{task_id}",
    response_model=A2ATask,
)
async def get_task(
    x_consumer_username: Annotated[str, Header()],
    task_id: str,
    history_length: Annotated[int | None, Query(alias="historyLength")] = None,
) -> A2ATask:
    """Return the latest recorded task runtime state."""

    task = _TASKS.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="A2A task not found")
    if history_length is None:
        return task
    history = [] if history_length <= 0 else task.history[-history_length:]
    return task.model_copy(update={"history": history})


@a2a_router.get(  # type: ignore[misc]
    "/tasks/{task_id}/events",
    response_model=A2ATaskEvents,
)
async def get_task_events(
    x_consumer_username: Annotated[str, Header()],
    task_id: str,
) -> A2ATaskEvents:
    """Return recorded task status and artifact events."""

    if task_id not in _TASKS:
        raise HTTPException(status_code=404, detail="A2A task not found")
    return A2ATaskEvents(events=_TASK_EVENTS.get(task_id, []))
