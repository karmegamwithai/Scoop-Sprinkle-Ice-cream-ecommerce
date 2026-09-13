"""
Supabase database client.

Provides generic CRUD helpers for the Django application.

Expected Supabase tables:
    users
    products
    orders
    order_items

Each table should have an auto-incrementing/identity `id` column.
"""

import datetime
import threading
from typing import Any
from decimal import Decimal

from django.conf import settings
from supabase import Client, create_client


# ---------------------------------------------------------------------------
# Supabase client
# ---------------------------------------------------------------------------

_lock = threading.Lock()
_client: Client | None = None


def _get_client() -> Client:
    """
    Lazily create and cache the Supabase client.
    """

    global _client

    if _client is None:
        with _lock:
            if _client is None:
                _client = create_client(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_KEY,
                )

    return _client


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def now_str() -> str:
    """
    Return the current datetime as an ISO formatted string.
    """

    return datetime.datetime.now().isoformat()


# ---------------------------------------------------------------------------
# READ
# ---------------------------------------------------------------------------

def get_all_rows(table_name: str) -> list[dict[str, Any]]:
    """
    Return all rows from a Supabase table.
    """

    response = (
        _get_client()
        .table(table_name)
        .select("*")
        .execute()
    )

    return response.data or []


def get_row_by_id(
    table_name: str,
    row_id: int | str,
) -> dict[str, Any] | None:
    """
    Return one row where id == row_id.
    """

    response = (
        _get_client()
        .table(table_name)
        .select("*")
        .eq("id", row_id)
        .limit(1)
        .execute()
    )

    return response.data[0] if response.data else None


def get_rows_by_field(
    table_name: str,
    field: str,
    value: Any,
) -> list[dict[str, Any]]:
    """
    Return all rows where field == value.
    """

    response = (
        _get_client()
        .table(table_name)
        .select("*")
        .eq(field, value)
        .execute()
    )

    return response.data or []


# ---------------------------------------------------------------------------
# CREATE
# ---------------------------------------------------------------------------

def insert_row(
    table_name: str,
    data: dict[str, Any],
) -> dict[str, Any]:
    """
    Insert a new row.

    Do not manually provide `id` if the Supabase/PostgreSQL
    table uses an identity/serial column.
    """

    data = data.copy()

    # Let PostgreSQL generate the ID.
    data.pop("id", None)

    response = (
        _get_client()
        .table(table_name)
        .insert(data)
        .execute()
    )

    return response.data[0] if response.data else data


# ---------------------------------------------------------------------------
# UPDATE
# ---------------------------------------------------------------------------

def update_row(
    table_name: str,
    row_id: int | str,
    data: dict[str, Any],
) -> dict[str, Any] | None:
    """
    Update a row where id == row_id.
    """

    data = data.copy()

    # Never update the primary key.
    data.pop("id", None)

    response = (
        _get_client()
        .table(table_name)
        .update(data)
        .eq("id", row_id)
        .execute()
    )

    return response.data[0] if response.data else None


# ---------------------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------------------

def delete_row(
    table_name: str,
    row_id: int | str,
) -> bool:
    """
    Delete a row where id == row_id.

    Returns:
        True  -> row deleted
        False -> no row found/deleted
    """

    response = (
        _get_client()
        .table(table_name)
        .delete()
        .eq("id", row_id)
        .execute()
    )

    return bool(response.data)