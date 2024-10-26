from typing import Optional

from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun

import requests

class LEDLightControl(BaseTool):
    """ LED Light Control Tool """
    name = "LEDLightControl"
    description = """
      Use this tool to control the LED Light.
      You must provide the location of the LED Light that you want to control. For example: bedroom, kitchen.
      Also, you must provide the requested status: on or off.
      Please provide the parameters always in this order: location, status.
    """

    def _run(
        self, parameters: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""

        location, status = parameters.split(",")

        location = location.strip()
        status = status.strip()

        if (status == "on"):
          requests.get("http://192.168.1.122/set?b=128")
        else:
          requests.get("http://192.168.1.122/set?b=1")

        return f"The LED Light in {location} has been successfully turned {status}"
