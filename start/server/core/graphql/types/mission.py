from typing import Literal, Optional

from ariadne import ObjectType

from core.graphql import GraphQLResolveInfo
from core.models import Mission

PatchSize = Literal["SMALL", "LARGE"]

mission = ObjectType("Mission")


@mission.field("mission_patch")
def resolve_mission_mission_patch(
    obj: Mission, info: GraphQLResolveInfo, size: PatchSize = "LARGE"
) -> Optional[str]:
    mission_patch: Optional[str] = obj.links[
        "mission_patch_small" if size == "SMALL" else "mission_patch"
    ]
    return mission_patch
