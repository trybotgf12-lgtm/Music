"""In-memory per-chat song queue. Resets on bot restart."""

queues: dict[int, list[dict]] = {}


def get_queue(chat_id: int) -> list[dict]:
    return queues.setdefault(chat_id, [])


def add_to_queue(chat_id: int, item: dict) -> int:
    q = get_queue(chat_id)
    q.append(item)
    return len(q)


def pop_next(chat_id: int) -> dict | None:
    q = get_queue(chat_id)
    if q:
        q.pop(0)
    return q[0] if q else None


def current(chat_id: int) -> dict | None:
    q = get_queue(chat_id)
    return q[0] if q else None


def clear_queue(chat_id: int) -> None:
    queues[chat_id] = []
