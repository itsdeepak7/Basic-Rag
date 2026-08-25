"""step 5: wrap the retrieval as a tool the agent can call."""

from langchain.tools import tool

def create_search_tool(retriever):
    """return a @tool function that searches the hr policy document."""
    @tool
    def search_hr_policy(question:str)->str:
        """search the hr policy document fir information about tleave,work rfrom home,probation, notice period ,reimbursement,code of conduct , holidays, or exit."""
        matching_chunks = retriever.invoke(question)
        return "\n\n".join(chunk.page_content for chunk in matching_chunks)

    return search_hr_policy

