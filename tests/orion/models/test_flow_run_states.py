import datetime
from uuid import uuid4

import pendulum
import pytest

from prefect.orion import models
from prefect.orion import schemas
from prefect.orion.schemas.states import Running, Scheduled, StateType


class TestCreateFlowRunState:
    async def test_create_flow_run_state_succeeds(self, flow_run, session):
        flow_run_state = (
            await models.flow_run_states.set_flow_run_state(
                session=session,
                flow_run_id=flow_run.id,
                state=Running(),
            )
        ).state
        assert flow_run_state.name == "Running"
        assert flow_run_state.type == StateType.RUNNING

    async def test_run_details_are_updated_entering_running(self, flow_run, session):
        frs = await models.flow_run_states.set_flow_run_state(
            session=session,
            flow_run_id=flow_run.id,
            state=Scheduled(),
        )

        await session.refresh(flow_run)

        assert flow_run.start_time is None
        assert flow_run.run_count == 0
        assert flow_run.total_run_time == datetime.timedelta(0)

        dt = pendulum.now("UTC")
        frs2 = await models.flow_run_states.set_flow_run_state(
            session=session,
            flow_run_id=flow_run.id,
            state=Running(timestamp=dt),
        )
        await session.refresh(flow_run)

        assert flow_run.start_time == dt
        assert flow_run.run_count == 1
        assert flow_run.total_run_time == datetime.timedelta(0)
        assert flow_run.estimated_run_time > datetime.timedelta(0)

        dt2 = pendulum.now("utc")
        frs3 = await models.flow_run_states.set_flow_run_state(
            session=session,
            flow_run_id=flow_run.id,
            state=Running(timestamp=dt2),
            # running / running isn't usually allowed
            force=True,
        )
        await session.commit()
        await session.refresh(flow_run)
        assert flow_run.start_time == dt
        assert flow_run.run_count == 2
        assert flow_run.total_run_time == (dt2 - dt)
        assert flow_run.estimated_run_time > (dt2 - dt)

    async def test_database_is_not_updated_when_no_transition_takes_place(
        self, flow_run, session
    ):

        # place the run in a scheduled state in the future
        frs = await models.flow_run_states.set_flow_run_state(
            session=session,
            flow_run_id=flow_run.id,
            state=Scheduled(scheduled_time=pendulum.now().add(months=1)),
        )

        # attempt to put the run in a pending state, which will tell the transition to WAIT
        frs2 = await models.flow_run_states.set_flow_run_state(
            session=session, flow_run_id=flow_run.id, state=Running()
        )

        assert frs2.status == schemas.responses.SetStateStatus.WAIT
        # the original state remains in place
        await session.refresh(flow_run)
        assert flow_run.state.id == frs.state.id


class TestReadFlowRunState:
    async def test_read_flow_run_state(self, flow_run, session):
        # create a flow run to read
        flow_run_state = (
            await models.flow_run_states.set_flow_run_state(
                session=session,
                flow_run_id=flow_run.id,
                state=Running(),
            )
        ).state

        read_flow_run_state = await models.flow_run_states.read_flow_run_state(
            session=session, flow_run_state_id=flow_run_state.id
        )
        assert flow_run_state == read_flow_run_state.as_state()

    async def test_read_flow_run_state_returns_none_if_does_not_exist(self, session):
        result = await models.flow_run_states.read_flow_run_state(
            session=session, flow_run_state_id=uuid4()
        )

        assert result is None


class TestReadFlowRunStates:
    async def test_flow_run_states(self, session, flow_run, flow_run_states):
        flow_run_states_by_flow_run_id = (
            await models.flow_run_states.read_flow_run_states(
                session=session, flow_run_id=flow_run.id
            )
        )
        assert len(flow_run_states_by_flow_run_id) == len(flow_run_states)

    async def test_flow_run_states_filters_by_flow_run_id(self, session):
        # query for states using a random flow run id
        flow_run_states_by_flow_run_id = (
            await models.flow_run_states.read_flow_run_states(
                session=session, flow_run_id=uuid4()
            )
        )
        assert len(flow_run_states_by_flow_run_id) == 0


class TestDeleteFlowRunState:
    async def test_delete_flow_run_state(self, flow_run, session):
        # create a flow run to read
        flow_run_state = (
            await models.flow_run_states.set_flow_run_state(
                session=session,
                flow_run_id=flow_run.id,
                state=Running(),
            )
        ).state

        assert await models.flow_run_states.delete_flow_run_state(
            session=session, flow_run_state_id=flow_run_state.id
        )

        # make sure the flow run state is deleted
        result = await models.flow_run_states.read_flow_run_state(
            session=session, flow_run_state_id=flow_run_state.id
        )
        assert result is None

    async def test_delete_flow_run_state_returns_false_if_does_not_exist(self, session):
        result = await models.flow_run_states.delete_flow_run_state(
            session=session, flow_run_state_id=uuid4()
        )
        assert not result
