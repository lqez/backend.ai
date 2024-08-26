from __future__ import annotations

from typing import TYPE_CHECKING, Mapping

import graphene
import sqlalchemy as sa
from dateutil.parser import parse as dtparse
from graphene.types.datetime import DateTime as GQLDateTime

from ..agent import AgentRow, AgentStatus
from ..base import (
    FilterExprArg,
    OrderExprArg,
    generate_sql_info_for_gql_connection,
)
from ..gql_relay import AsyncNode, Connection, ConnectionResolverResult
from ..minilang.ordering import OrderSpecItem, QueryOrderParser
from ..minilang.queryfilter import FieldSpecItem, QueryFilterParser, enum_field_getter

if TYPE_CHECKING:
    from ..gql import GraphQueryContext


class AgentNode(graphene.ObjectType):
    class Meta:
        interfaces = (AsyncNode,)

    status = graphene.String(description="Status of the agent.")
    status_changed = GQLDateTime()
    region = graphene.String(description="Region of the agent.")
    scaling_group = graphene.String(description="Scaling group of the agent.")
    schedulable = graphene.Boolean()
    available_slots = graphene.JSONString()
    occupied_slots = graphene.JSONString()
    addr = graphene.String(description="Address of the agent.")
    architecture = graphene.String(description="Architecture of the agent.")
    first_contact = GQLDateTime()
    lost_at = GQLDateTime()
    version = graphene.String(description="Version of the agent.")
    compute_plugins = graphene.JSONString()
    auto_terminate_abusing_kernel = graphene.Boolean()

    @classmethod
    def from_row(cls, row: AgentRow) -> AgentNode:
        return cls(
            id=row.id,
            status=row.status.name,
            status_changed=row.status_changed,
            region=row.region,
            scaling_group=row.scaling_group,
            schedulable=row.schedulable,
            available_slots=row.available_slots.to_json(),
            occupied_slots=row.occupied_slots.to_json(),
            addr=row.addr,
            architecture=row.architecture,
            first_contact=row.first_contact,
            lost_at=row.lost_at,
            version=row.version,
            compute_plugins=row.compute_plugins,
            auto_terminate_abusing_kernel=row.auto_terminate_abusing_kernel,
        )

    @classmethod
    async def get_node(cls, info: graphene.ResolveInfo, id) -> AgentNode:
        graph_ctx: GraphQueryContext = info.context

        _, agent_id = AsyncNode.resolve_global_id(info, id)
        query = sa.select(AgentRow).where(AgentRow.id == agent_id)
        async with graph_ctx.db.begin_readonly_session() as db_session:
            agent_row = (await db_session.scalars(query)).first()
            return cls.from_row(agent_row)

    _queryfilter_fieldspec: Mapping[str, FieldSpecItem] = {
        "id": ("id", None),
        "status": ("status", enum_field_getter(AgentStatus)),
        "status_changed": ("status_changed", dtparse),
        "region": ("region", None),
        "scaling_group": ("scaling_group", None),
        "schedulable": ("schedulable", None),
        "addr": ("addr", None),
        "first_contact": ("first_contact", dtparse),
        "lost_at": ("lost_at", dtparse),
        "version": ("version", None),
        "architecture": ("architecture", None),
        "compute_plugins": ("compute_plugins", None),
        "auto_terminate_abusing_kernel": ("auto_terminate_abusing_kernel", None),
    }

    _queryorder_colmap: Mapping[str, OrderSpecItem] = {
        "id": ("id", None),
        "status": ("status", None),
        "status_changed": ("status_changed", None),
        "region": ("region", None),
        "scaling_group": ("scaling_group", None),
        "schedulable": ("schedulable", None),
        "first_contact": ("first_contact", None),
        "lost_at": ("lost_at", None),
        "version": ("version", None),
        "architecture": ("architecture", None),
    }

    @classmethod
    async def get_connection(
        cls,
        info: graphene.ResolveInfo,
        filter_expr: str | None = None,
        order_expr: str | None = None,
        offset: int | None = None,
        after: str | None = None,
        first: int | None = None,
        before: str | None = None,
        last: int | None = None,
    ) -> ConnectionResolverResult:
        graph_ctx: GraphQueryContext = info.context
        _filter_arg = (
            FilterExprArg(filter_expr, QueryFilterParser(cls._queryfilter_fieldspec))
            if filter_expr is not None
            else None
        )
        _order_expr = (
            OrderExprArg(order_expr, QueryOrderParser(cls._queryorder_colmap))
            if order_expr is not None
            else None
        )
        (
            query,
            cnt_query,
            _,
            cursor,
            pagination_order,
            page_size,
        ) = generate_sql_info_for_gql_connection(
            info,
            AgentRow,
            AgentRow.id,
            _filter_arg,
            _order_expr,
            offset,
            after=after,
            first=first,
            before=before,
            last=last,
        )
        async with graph_ctx.db.begin_readonly_session() as db_session:
            agent_rows = (await db_session.scalars(query)).all()
            result = [cls.from_row(row) for row in agent_rows]

            total_cnt = await db_session.scalar(cnt_query)
            return ConnectionResolverResult(result, cursor, pagination_order, page_size, total_cnt)


class AgentConnection(Connection):
    class Meta:
        node = AgentNode
