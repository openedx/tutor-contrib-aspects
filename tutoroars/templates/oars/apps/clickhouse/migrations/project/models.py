from clickhouse_sqlalchemy import get_declarative_base, types, engines, MaterializedView, select
from sqlalchemy import create_engine, Column, MetaData, func

uri = '{{ CLICKHOUSE_ADMIN_SQLALCHEMY_URI_ALEMBIC }}'

engine = create_engine(uri)
metadata = MetaData(bind=engine)

Base = get_declarative_base(metadata=metadata)


class Statistics(Base):
    date = Column(types.Date, primary_key=True)
    sign = Column(types.Int8, nullable=False)
    grouping = Column(types.Int32, nullable=False)
    metric1 = Column(types.Int32, nullable=False)
    metric2 = Column(types.Int32, nullable=False, clickhouse_codec=('DoubleDelta', 'ZSTD'))

    __table_args__ = (
        engines.CollapsingMergeTree(sign, partition_by=func.toYYYYMM(date), order_by=(date, grouping)),
    )
