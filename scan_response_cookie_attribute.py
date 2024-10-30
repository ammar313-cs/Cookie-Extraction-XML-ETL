import sqlalchemy as sa
from sqlalchemy import orm


class ScanResponseCookieAttribute(orm.DeclarativeBase):
    """
    Stores attribute names for set-cookies(response).
    """

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    attribute_name: orm.Mapped[str] = orm.mapped_column(
        sa.Unicode(256), nullable=False, unique=True
    )
