from enum import Enum


class AuditStatus(Enum):
    NOT_VIEWED = 'NOT_VIEWED'
    VIEWED = 'VIEWED'
    SENT_TICKET = 'SENT_TICKET'
    TICKET_FINISHED = 'TICKET_FINISHED'
