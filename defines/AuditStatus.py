from enum import Enum


class AuditStatus(Enum):
    NOT_VIEWED = 'NOT_VIEWED'
    PASS_VIEW = 'PASS_VIEW'
    VIEWED = 'VIEWED'
    SENT_TICKET = 'SENT_TICKET'
    TICKET_FINISHED = 'TICKET_FINISHED'
