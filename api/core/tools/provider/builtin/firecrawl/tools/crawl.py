from typing import Any

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.provider.builtin.firecrawl.firecrawl_appx import FirecrawlApp, get_array_params, get_json_params
from core.tools.tool.builtin_tool import BuiltinTool


class CrawlTool(BuiltinTool):
    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]) -> ToolInvokeMessage:
        """
        the crawlerOptions and pageOptions comes from doc here:
        https://docs.firecrawl.dev/api-reference/endpoint/crawl
        """
        app = FirecrawlApp(
            api_key=self.runtime.credentials["firecrawl_api_key"], base_url=self.runtime.credentials["base_url"]
        )
        scrapeOptions = {}
        formats = []

        wait_for_results = tool_parameters.get("wait_for_results", True)

        if tool_parameters.get("includeHtml", False):
            formats.append("html")

        if tool_parameters.get("includeRawHtml", False):
            formats.append("rawHtml")

        if tool_parameters.get("screenshot", False):
            formats.append("screenshot")

        scrapeOptions["headers"] = get_json_params(tool_parameters, "headers")
        scrapeOptions["onlyMainContent"] = tool_parameters.get("onlyMainContent", False)
        scrapeOptions["waitFor"] = tool_parameters.get("waitFor", 0)
        scrapeOptions["includeTags"] = get_array_params(tool_parameters, "onlyIncludeTags")
        scrapeOptions["excludeTags"] = get_array_params(tool_parameters, "removeTags")
        scrapeOptions["formats"] = formats

        crawl_result = app.crawl_url(
            url=tool_parameters["url"], 
            wait=wait_for_results, 
            includePaths=get_array_params(tool_parameters, "includes"),
            excludePaths=get_array_params(tool_parameters, "excludes"),
            allowBackwardLinks=tool_parameters.get("allowBackwardCrawling", False),
            allowExternalLinks=tool_parameters.get("allowExternalContentLinks", False),
            maxDepth=tool_parameters.get("maxDepth"),
            ignoreSitemap=tool_parameters.get("ignoreSitemap", False),
            limit=tool_parameters.get("limit", 5),
            scrapeOptions=scrapeOptions
        )

        return self.create_json_message(crawl_result)
