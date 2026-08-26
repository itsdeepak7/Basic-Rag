"""step 5: wrap the retrieval as a tool the agent can call."""

from langchain.tools import tool

from hr_assistant.logger import get_logger

logger = get_logger(__name__)


def create_search_tool(retriever):
    """return a @tool function that searches the hr policy document."""
    @tool
    def search_hr_policy(question:str)->str:
        """search the hr policy document fir information about tleave,work rfrom home,probation, notice period ,reimbursement,code of conduct , holidays, or exit."""
        logger.info("search_hr_policy called with query: %s", question)
        matching_chunks = retriever.invoke(question)
        logger.info("Found %d matching chunk(s)", len(matching_chunks))
        return "\n\n".join(chunk.page_content for chunk in matching_chunks)

    return search_hr_policy

