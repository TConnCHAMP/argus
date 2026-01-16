"""
This module contains all thread-related routes for the LightRAG API.
Threads allow organizing conversations with context persistence.
"""

import json
import os
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from lightrag.api.utils_api import get_combined_auth_dependency
from lightrag.utils import logger
from pydantic import BaseModel, Field
import uuid

router = APIRouter(tags=["threads"])


class ThreadMessage(BaseModel):
    """A single message in a thread."""

    role: str = Field(description="Message role: 'user' or 'assistant'")
    content: str = Field(description="Message content")
    timestamp: str = Field(description="ISO 8601 timestamp")


class CreateThreadRequest(BaseModel):
    """Request to create a new thread."""

    title: Optional[str] = Field(default=None, description="Optional thread title")
    initial_message: Optional[str] = Field(default=None, description="Optional first message")


class UpdateThreadRequest(BaseModel):
    """Request to update thread metadata."""

    title: Optional[str] = Field(default=None, description="New thread title")


class AddMessageRequest(BaseModel):
    """Request to add a message to a thread."""

    role: str = Field(description="Message role: 'user' or 'assistant'")
    content: str = Field(min_length=1, description="Message content")


class Thread(BaseModel):
    """Complete thread data."""

    id: str = Field(description="Unique thread identifier")
    title: str = Field(description="Thread title")
    created_at: str = Field(description="ISO 8601 creation timestamp")
    updated_at: str = Field(description="ISO 8601 last update timestamp")
    messages: List[ThreadMessage] = Field(default_factory=list, description="Thread messages")


class ThreadListItem(BaseModel):
    """Thread summary for list view."""

    id: str = Field(description="Unique thread identifier")
    title: str = Field(description="Thread title")
    created_at: str = Field(description="ISO 8601 creation timestamp")
    updated_at: str = Field(description="ISO 8601 last update timestamp")
    message_count: int = Field(description="Number of messages in thread")
    preview: Optional[str] = Field(default=None, description="Preview of last message")


class ThreadStorage:
    """Simple JSON-based thread storage."""

    def __init__(self, working_dir: str):
        self.threads_dir = os.path.join(working_dir, "threads")
        os.makedirs(self.threads_dir, exist_ok=True)

    def _thread_path(self, thread_id: str) -> str:
        return os.path.join(self.threads_dir, f"{thread_id}.json")

    def create_thread(self, title: Optional[str] = None, initial_message: Optional[str] = None) -> Thread:
        """Create a new thread."""
        thread_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat() + "Z"

        messages = []
        if initial_message:
            messages.append(ThreadMessage(
                role="user",
                content=initial_message,
                timestamp=now
            ))

        thread = Thread(
            id=thread_id,
            title=title or "New Conversation",
            created_at=now,
            updated_at=now,
            messages=messages
        )

        with open(self._thread_path(thread_id), 'w', encoding='utf-8') as f:
            json.dump(thread.model_dump(), f, ensure_ascii=False, indent=2)

        return thread

    def get_thread(self, thread_id: str) -> Optional[Thread]:
        """Get a thread by ID."""
        path = self._thread_path(thread_id)
        if not os.path.exists(path):
            return None

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Thread(**data)
        except Exception as e:
            logger.error(f"Error loading thread {thread_id}: {e}")
            return None

    def update_thread(self, thread_id: str, title: Optional[str] = None) -> Optional[Thread]:
        """Update thread metadata."""
        thread = self.get_thread(thread_id)
        if not thread:
            return None

        if title is not None:
            thread.title = title
        thread.updated_at = datetime.utcnow().isoformat() + "Z"

        with open(self._thread_path(thread_id), 'w', encoding='utf-8') as f:
            json.dump(thread.model_dump(), f, ensure_ascii=False, indent=2)

        return thread

    def delete_thread(self, thread_id: str) -> bool:
        """Delete a thread."""
        path = self._thread_path(thread_id)
        if not os.path.exists(path):
            return False

        try:
            os.remove(path)
            return True
        except Exception as e:
            logger.error(f"Error deleting thread {thread_id}: {e}")
            return False

    def list_threads(self) -> List[ThreadListItem]:
        """List all threads."""
        threads = []

        if not os.path.exists(self.threads_dir):
            return threads

        for filename in os.listdir(self.threads_dir):
            if not filename.endswith('.json'):
                continue

            try:
                with open(os.path.join(self.threads_dir, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)

                thread = Thread(**data)
                preview = None
                if thread.messages:
                    last_msg = thread.messages[-1].content
                    preview = last_msg[:100] + "..." if len(last_msg) > 100 else last_msg

                threads.append(ThreadListItem(
                    id=thread.id,
                    title=thread.title,
                    created_at=thread.created_at,
                    updated_at=thread.updated_at,
                    message_count=len(thread.messages),
                    preview=preview
                ))
            except Exception as e:
                logger.error(f"Error loading thread from {filename}: {e}")

        # Sort by updated_at (most recent first)
        threads.sort(key=lambda t: t.updated_at, reverse=True)
        return threads

    def add_message(self, thread_id: str, role: str, content: str) -> Optional[Thread]:
        """Add a message to a thread."""
        thread = self.get_thread(thread_id)
        if not thread:
            return None

        message = ThreadMessage(
            role=role,
            content=content,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

        thread.messages.append(message)
        thread.updated_at = message.timestamp

        with open(self._thread_path(thread_id), 'w', encoding='utf-8') as f:
            json.dump(thread.model_dump(), f, ensure_ascii=False, indent=2)

        return thread


def create_thread_routes(working_dir: str, api_key: Optional[str] = None):
    """Create thread management routes."""
    storage = ThreadStorage(working_dir)
    combined_auth = get_combined_auth_dependency(api_key)

    @router.post("/threads", response_model=Thread, dependencies=[Depends(combined_auth)])
    async def create_thread(request: CreateThreadRequest):
        """
        Create a new conversation thread.

        Threads allow organizing conversations with persistent context.
        Each thread maintains its own message history.

        Args:
            request: Thread creation parameters (optional title and initial message)

        Returns:
            Thread: The newly created thread
        """
        try:
            thread = storage.create_thread(
                title=request.title,
                initial_message=request.initial_message
            )
            return thread
        except Exception as e:
            logger.error(f"Error creating thread: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/threads", response_model=List[ThreadListItem], dependencies=[Depends(combined_auth)])
    async def list_threads():
        """
        List all conversation threads.

        Returns a summary of all threads sorted by last update time.

        Returns:
            List[ThreadListItem]: List of thread summaries
        """
        try:
            return storage.list_threads()
        except Exception as e:
            logger.error(f"Error listing threads: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/threads/{thread_id}", response_model=Thread, dependencies=[Depends(combined_auth)])
    async def get_thread(thread_id: str):
        """
        Get a specific thread with all messages.

        Args:
            thread_id: The thread identifier

        Returns:
            Thread: Complete thread data including all messages

        Raises:
            HTTPException: 404 if thread not found
        """
        thread = storage.get_thread(thread_id)
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
        return thread

    @router.patch("/threads/{thread_id}", response_model=Thread, dependencies=[Depends(combined_auth)])
    async def update_thread(thread_id: str, request: UpdateThreadRequest):
        """
        Update thread metadata.

        Currently supports updating the thread title.

        Args:
            thread_id: The thread identifier
            request: Update parameters

        Returns:
            Thread: Updated thread data

        Raises:
            HTTPException: 404 if thread not found
        """
        thread = storage.update_thread(thread_id, title=request.title)
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
        return thread

    @router.delete("/threads/{thread_id}", dependencies=[Depends(combined_auth)])
    async def delete_thread(thread_id: str):
        """
        Delete a thread.

        Permanently removes a thread and all its messages.

        Args:
            thread_id: The thread identifier

        Returns:
            dict: Success confirmation

        Raises:
            HTTPException: 404 if thread not found
        """
        success = storage.delete_thread(thread_id)
        if not success:
            raise HTTPException(status_code=404, detail="Thread not found")
        return {"status": "success", "message": "Thread deleted"}

    @router.post("/threads/{thread_id}/messages", response_model=Thread, dependencies=[Depends(combined_auth)])
    async def add_message(thread_id: str, request: AddMessageRequest):
        """
        Add a message to a thread.

        Appends a new message to the thread's conversation history.

        Args:
            thread_id: The thread identifier
            request: Message data (role and content)

        Returns:
            Thread: Updated thread with the new message

        Raises:
            HTTPException: 404 if thread not found
        """
        thread = storage.add_message(thread_id, request.role, request.content)
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
        return thread

    return router
