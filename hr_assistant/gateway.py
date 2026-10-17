"""Step 6b: route the LLM through the Portkey gateway.

Instead of calling Groq directly, the main LLM call goes through Portkey.
Portkey stores the real Groq credentials behind a "slug" (set up once in
the Portkey dashboard) - our code never sees the raw Groq key.
"""

import json
from langchain_openai import ChatOpenAI
from portkey_ai import PORTKEY_GATEWAY_URL,createHeaders
from langchain_groq import ChatGroq
from hr_assistant.config import PORTKEY_CONFIG_SLUG


from hr_assistant import config
from hr_assistant.logger import get_logger


logger = get_logger(__name__)

# The one Groq integration set up in the Portkey dashboard for this
# workspace (see module docstring for why there's only one).
PRIMARY_PROVIDER = "@backupllm"
JUDGE_PROVIDER = "@judge"

PRIMARY_TARGET = {'provider':"@backupllm",
                  "override_params":{"model":config.LLM_MODEL_NAME}}


FALLBACK_TARGET = {'provider':"@hrpolicybackup",
                  "override_params":{"model": "openai/gpt-oss-20b"}}

GATEWAY_CONFIG = {
    "strategy":{
        "mode":"fallback"
        },
    "targets":[PRIMARY_TARGET,FALLBACK_TARGET]
}

#gateway features
#loadbalncing
#model routing 
#caching 
#fallback



# acces our gateway
#portkey ai
#openai compatible to acces 
  

GATEWAY_CONFIG = {
    "strategy": {
        "mode": "fallback"
    },
    "targets": [PRIMARY_TARGET, FALLBACK_TARGET],
}

# 3. Initialize ChatOpenAI pointing to Portkey Gateway
def get_gateway_llm() -> ChatOpenAI:
    """Return a ChatOpenAI model routed via Portkey Gateway with fallback routing."""
    logger.info("Routing LLM calls through Portkey Gateway with fallback strategy")

    # createHeaders accepts a dictionary object directly for the config parameter
    headers = createHeaders(
        api_key=config.PORTKEY_API_KEY.strip(),
        config=PORTKEY_CONFIG_SLUG
    )

    return ChatOpenAI(
        model=config.LLM_MODEL_NAME,
        api_key=config.PORTKEY_API_KEY.strip(),
        base_url=PORTKEY_GATEWAY_URL,
        default_headers=headers,
    )


def get_judge_llm() ->ChatOpenAI:
    """Return a judge model routed through Portkey, same slug as the main app."""
    logger.info("Routing Judge LLM calls through Portkey Gateway with fallback strategy")

    headers = createHeaders(
        api_key=config.PORTKEY_API_KEY.strip(),
        virtual_key=JUDGE_PROVIDER
    )

    return ChatOpenAI(
        model=config.JUDGE_MODEL_NAME,
        api_key="portkey",
        base_url=PORTKEY_GATEWAY_URL,
        default_headers=headers,
    )