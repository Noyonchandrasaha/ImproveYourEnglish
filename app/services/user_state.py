user_states = {}

def get_user_state(user_id: int):
    return user_states.get(user_id, {})

def set_user_state(user_id: int, key: str, value):
    user_states.setdefault(user_id, {})[key] = value

def get_user_topics(user_id: int):
    return user_states.get(user_id, {}).get("topics", [])

def update_user_topics(user_id: int, topic: str):
    state = user_states.setdefault(user_id, {})
    topics = state.setdefault("topics", [])
    if topic not in topics:
        topics.append(topic)

def set_bangla_sentence(user_id: int, sentence: str):
    set_user_state(user_id, "bangla_sentence", sentence)
    set_user_state(user_id, "awaiting_translation", True)

def get_bangla_sentence(user_id: int):
    return user_states.get(user_id, {}).get("bangla_sentence")

def clear_user_state(user_id: int):
    if user_id in user_states:
        del user_states[user_id]

def get_next_topic(user_id: int):
    topic_sequence = [
        "Tenses",
        "Sentence Structure",
        "Subject-Verb Agreement",
        "Articles",
        "Active and Passive Voice",
        "Modal Verbs",
        "Conditionals",
        "Direct and Indirect Speech"
    ]
    completed = get_user_topics(user_id)
    for topic in topic_sequence:
        if topic not in completed:
            return topic
    return None
