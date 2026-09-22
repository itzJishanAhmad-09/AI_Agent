from ddgs import DDGS

def search_web(query: str, max_results: int = 5) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return "No results found."
        lines = []
        for i, r in enumerate(results, 1):
            lines.append(f"{i}. {r['title']}")
            lines.append(f"   {r['href']}")
            lines.append(f"   {r['body'][:200]}")
            lines.append("")
        return "\n".join(lines)
    except Exception as e:
        return f"Error searching web: {e}"