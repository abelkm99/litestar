from __future__ import annotations

from typing import TYPE_CHECKING, Any

from litestar.exceptions import MissingDependencyException

__all__ = ("get_route_details_from_scope",)


try:
    import opentelemetry  # noqa: F401
except ImportError as e:
    raise MissingDependencyException("opentelemetry") from e

from opentelemetry.semconv.trace import SpanAttributes

if TYPE_CHECKING:
    from litestar.types import Scope


def get_route_details_from_scope(scope: Scope) -> tuple[str, dict[Any, str]]:
    """Retrieve the span name and attributes from the ASGI scope.

    Args:
        scope: The ASGI scope instance.

    Returns:
        A tuple of the span name and a dict of attrs.
    """

    path = scope.get("path", "").strip()
    method = str(scope.get("method", "")).strip()

    if method and path:  # http
        return f"{method} {path}", {SpanAttributes.HTTP_ROUTE: f"{method} {path}"}

    return path, {SpanAttributes.HTTP_ROUTE: path}  # websocket
