# -*- coding: utf-8 -*-
"""
Useful ajax middleware classes.

"""
import json

from django.contrib import messages


class AjaxMessaging(object):
    def process_response(self, request, response):
        if request.is_ajax():
            content_type = response.get('Content-Type')
            if content_type in ["application/javascript", "application/json"]:
                try:
                    content = json.loads(response.content)
                except ValueError:
                    return response

                django_messages = []

                for message in messages.get_messages(request):
                    django_messages.append({
                        "level": message.level,
                        "message": message.message,
                        "extra_tags": message.tags,
                    })

                content['django_messages'] = django_messages
                response.content = json.dumps(content)
        return response
