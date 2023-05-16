"""Test CrowdStrike events schemas."""
import pytest
from pydantic import ValidationError

from crowdstrike_telemetry.schemas import CrowdStrikeEventSchema, FileInfoSchema


@pytest.mark.asyncio
async def test_file_info_schema_valid(session_faker):
    """
    Test create valid FileInfoSchema object.

    Args:
        session_faker: Faker
    """
    file_path = session_faker.file_path()
    file_info = FileInfoSchema(path=file_path)

    assert file_info.path == file_path


@pytest.mark.asyncio
async def test_file_info_schema_invalid():
    """Test create invalid FileInfoSchema object."""
    with pytest.raises(ValidationError):
        FileInfoSchema()


@pytest.mark.asyncio
async def test_crowdstrike_event_schema_valid(session_faker):
    """
    Test create valid CrowdStrikeEventSchema object.

    Args:
        session_faker: Faker
    """
    file_path = session_faker.file_path()
    bucket = session_faker.word()

    event_data = {"bucket": bucket, "files": [{"path": file_path}]}
    event = CrowdStrikeEventSchema(**event_data)

    assert event.bucket == bucket
    assert len(event.files) == 1
    assert event.files[0].path == file_path


@pytest.mark.asyncio
async def test_crowdstrike_event_schema_invalid():
    """Test create invalid CrowdStrikeEventSchema object."""
    with pytest.raises(ValidationError):
        CrowdStrikeEventSchema()
