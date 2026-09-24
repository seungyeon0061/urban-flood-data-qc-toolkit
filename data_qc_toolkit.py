import os
import sys
from typing import List

from superagi.tools.base_tool import BaseTool, BaseToolkit

# 같은 폴더의 data_qc_tool.py를 찾을 수 있게 경로 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
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
