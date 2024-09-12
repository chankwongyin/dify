from typing import Any

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.provider.builtin.firecrawl.firecrawl_appx import FirecrawlApp, get_array_params, get_json_params
from core.tools.tool.builtin_tool import BuiltinTool


class ScrapeTool(BuiltinTool):
    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]) -> ToolInvokeMessage:
        """
        the pageOptions and extractorOptions comes from doc here:
        https://docs.firecrawl.dev/api-reference/endpoint/scrape
        """
        app = FirecrawlApp(
            api_key=self.runtime.credentials["firecrawl_api_key"], base_url=self.runtime.credentials["base_url"]
        )

        formatsOptions = []
        extractOptions = {}

        if tool_parameters.get("includeHtml", False):
            formatsOptions.append("html")

        if tool_parameters.get("includeRawHtml", False):
            formatsOptions.append("rawHtml")

        if tool_parameters.get("screenshot", False):
            formatsOptions.append("screenshot")

        extractOptions["systemPrompt"] = tool_parameters.get("systemPrompt", "")
        extractOptions["prompt"] = tool_parameters.get("extractionPrompt", "")
        extractOptions["schema"] = get_json_params(tool_parameters, "extractionSchema")

        crawl_result = app.scrape_url(
            url=tool_parameters["url"], 
            header=get_json_params(tool_parameters, "headers"), 
            includeTags=get_array_params(tool_parameters, "onlyIncludeTags"),
            excludeTags=get_array_params(tool_parameters, "removeTags"),
            onlyMainContent=tool_parameters.get("onlyMainContent", False),
            waitFor=tool_parameters.get("waitFor", 0),
            formats=formatsOptions,
            extract=extractOptions
        )

        return self.create_json_message(crawl_result)
