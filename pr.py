from datetime import datetime


def hide_field(field) -> str:
    return "***"


def format_time(field_timestamp):
    return field_timestamp.strftime()


def show_original(event_field):
    return event_field


class EventSerializer:
    def __init__(self, serialization_fields: dict) -> None:
        self.serialization_fields = serialization_fields

    def serialize(self, event):
        """
        transaformation : hide_field, format_time, show_original
        event : LogInEvent
        """
        data = {
            field: transformation(getattr(event, field))
            for field, transformation in self.serialization_fields.items()
        }
        return data


class Serialization:
    def __init__(self, **transformations) -> None:
        # 1. Serialization 메모리 할당되면서
        # serializer 클래스 변수로 EventSerializer 할당
        self.serializer = EventSerializer(transformations)
        print("1 -----", self.serializer)

    def __call__(self, event_class):
        # 2. event_class(LogInEvent) 할당 전에 데코레이터 실행
        print("2 ----- ", event_class)

        def serialize_method(event_instance):
            # 메모리 할당된 클래스
            return self.serializer.serialize(event_instance)

        # 메소드 바운딩

        event_class.serialize = serialize_method
        print("3 ----- ", event_class.serialize)

        # 메소드 바운딩된 LogInEvent 리턴
        return event_class


@Serialization(username=show_original, password=hide_field, ip=show_original)
class LogInEvent:
    def __init__(self, username, password, ip) -> None:
        self.username = username
        self.password = password
        self.ip = ip


event = LogInEvent("chanjong", "adwadaw", "127.0.0.1")

print("Final : ", event.serialize())
