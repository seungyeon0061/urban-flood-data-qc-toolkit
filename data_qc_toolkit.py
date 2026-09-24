from typing import List

from superagi.tools.base_tool import BaseTool
from superagi.tools.base_toolkit import BaseToolkit

try:
    from .data_qc_tool import DataQCTool
except ImportError:
    from data_qc_tool import DataQCTool


class DataQCToolkit(BaseToolkit):
    name: str = "Urban Flood Data QC Toolkit"
    description: str = (
        "Toolkit for quality control and validation of urban flood input data "
        "before flood-risk model inference."
    )

    def get_tools(self) -> List[BaseTool]:
        return [DataQCTool()]

    def get_env_keys(self) -> List[str]:
        return []
