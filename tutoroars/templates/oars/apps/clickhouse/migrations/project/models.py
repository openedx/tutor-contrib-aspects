from clickhouse_sqlalchemy import get_declarative_base, types, engines
from sqlalchemy import create_engine, Column, MetaData, func

uri = '{{ CLICKHOUSE_ADMIN_SQLALCHEMY_URI_ALEMBIC }}/{{ OARS_XAPI_DATABASE }}'

engine = create_engine(uri)
metadata = MetaData(bind=engine)

Base = get_declarative_base(metadata=metadata)


class XapiEventsAll(Base):
    __table_name__ = "xapi_events_all"
    emission_time = Column(types.DateTime, nullable=False, primary_key=True)
    event_id = Column(types.UUID, nullable=False, primary_key=True)
    event_str = Column(types.String, nullable=False)

    __table_args__ = (
        engines.MergeTree(
            partition_by=func.toYYYYMM(emission_time),
            order_by=("emission_time", "event_id"),
        ),
    )
