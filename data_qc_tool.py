import json
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
        "Returns a JSON string with status PASS, WARN, or FAIL and reasons."
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
        errors = []

        # FAIL 조건 (추론 불가)
        if rainfall_10min < 0 or rainfall_1h < 0:
            errors.append("Rainfall values cannot be negative.")
        if not timestamp:
            errors.append("Timestamp is missing.")
        if not grid_id:
            errors.append("grid_id is missing.")

        # WARN 조건 (추론은 가능하지만 주의)
        if rainfall_10min > rainfall_1h:
            warnings.append("10-minute rainfall exceeds 1-hour accumulated rainfall.")
        if water_level < 0:
            warnings.append("Water level is negative and should be checked.")

        if errors:
            status = "FAIL"
            ready = False
        elif warnings:
            status = "WARN"
            ready = True
        else:
            status = "PASS"
            ready = True

        result = {
            "status": status,
            "ready_for_inference": ready,
            "warnings": errors + warnings,
            "timestamp": timestamp,
            "grid_id": grid_id,
        }

        return json.dumps(result, ensure_ascii=False)
