from typing import Type
from pydantic import BaseModel, Field

from superagi.tools.base_tool import BaseTool


class DataQCInput(BaseModel):
    rainfall_10min: float = Field(..., description="10-minute rainfall in mm")
    rainfall_1h: float = Field(..., description="1-hour accumulated rainfall in mm")
    water_level: float = Field(..., description="Current observed water level")
    timestamp: str = Field(..., description="Observation timestamp")
    grid_id: str = Field(..., description="Spatial grid identifier")


class DataQCTool(BaseTool):
    name: str = "Urban Flood Data QC"
    args_schema: Type[BaseModel] = DataQCInput
    description: str = (
        "Checks whether urban flood input data are valid before flood-risk inference. "
        "Returns PASS, WARN, or FAIL with reasons."
    )

    def _execute(
        self,
        rainfall_10min: float,
        rainfall_1h: float,
        water_level: float,
        timestamp: str,
        grid_id: str,
    ):
        warnings = []

        if rainfall_10min < 0 or rainfall_1h < 0:
            return {
                "status": "FAIL",
                "ready_for_inference": False,
                "warnings": ["Rainfall values cannot be negative."]
            }

        if not timestamp:
            return {
                "status": "FAIL",
                "ready_for_inference": False,
                "warnings": ["Timestamp is missing."]
            }

        if not grid_id:
            return {
                "status": "FAIL",
                "ready_for_inference": False,
                "warnings": ["grid_id is missing."]
            }

        if rainfall_10min > rainfall_1h:
            warnings.append(
                "10-minute rainfall exceeds 1-hour accumulated rainfall."
            )

        if water_level < 0:
            warnings.append("Water level is negative and should be checked.")

        status = "WARN" if warnings else "PASS"

        return {
            "status": status,
            "ready_for_inference": True,
            "warnings": warnings,
            "timestamp": timestamp,
            "grid_id": grid_id
        }
