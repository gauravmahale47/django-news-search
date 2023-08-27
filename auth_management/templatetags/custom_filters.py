import json
from django import template
from datetime import datetime

register = template.Library()


@register.filter
def human_readable_time(value):
    now = datetime.now()
    published_time = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    time_difference = now - published_time

    if time_difference.days > 0:
        return f"{time_difference.days} days ago"
    elif time_difference.seconds // 3600 > 0:
        return f"{time_difference.seconds // 3600} hours ago"
    else:
        return f"{time_difference.seconds // 60} minutes ago"


@register.filter
def convert_json_to_dict(value):
    return json.loads(value).get("data")