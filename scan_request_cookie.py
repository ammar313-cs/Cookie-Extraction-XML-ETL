import sqlalchemy as sa
from sqlalchemy import orm

from .scan_item import ScanItem
from .scan_request_cookie_attribute import ScanRequestCookieAttribute


class ScanRequestCookie(orm.DeclarativeBase):
    """
    Stores request cookie values with references to attribute IDs and scan items.
    """

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.Unicode(256), nullable=False)
    value: orm.Mapped[str] = orm.mapped_column(sa.Unicode(1024), nullable=True)

    attribute_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("scan_request_cookie_attribute.id"), nullable=False
    )
    scan_item_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("scan_item.id"), nullable=False
    )

    scan_item: orm.Mapped["ScanItem"] = orm.relationship(backref="scan_request_cookies")
    attribute: orm.Mapped["ScanRequestCookieAttribute"] = orm.relationship()
