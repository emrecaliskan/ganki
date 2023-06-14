from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from langchain.callbacks.manager import CallbackManagerForChainRun
from langchain.chains import QAGenerationChain
from langchain.prompts.prompt import PromptTemplate

templ = """You are a smart assistant designed to help high school teachers come up with reading comprehension questions.
Given a piece of text, you must come up with a question and answer pair that can be used to test a student's reading comprehension abilities.
When coming up with this question/answer pair, you must respond in the following format:
```

{{
    "questions": [
        {{
            "question": "$YOUR_QUESTION_HERE",
            "answer": "$THE_ANSWER_HERE"
        }},
        {{
            "question": "$ANOTHER_QUESTION_HERE",
            "answer": "$ANOTHER_ANSWER_HERE"
        }},
    ]
}}
```

Everything between the ``` must be valid json.

In addition, you have to cover all important concepts in the text with at least one question/answer pair for every 100 words in the text.
For example, if the text is 1000 words long, you must come up with at least 10 question/answer pairs.

Please come up with a question/answer pair, in the specified JSON format, for the following text:
----------------
{text}"""
DEFAULT_PROMPT = PromptTemplate.from_template(templ)


class QAGenerationChainMod(QAGenerationChain):
    @classmethod
    def from_llm(cls, model, prompt: PromptTemplate = DEFAULT_PROMPT):
        return super().from_llm(model, prompt=prompt)

    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, List]:
        docs = self.text_splitter.create_documents([inputs[self.input_key]])
        results = self.llm_chain.generate(
            [{"text": d.page_content} for d in docs], run_manager=run_manager
        )
        responses = [json.loads(res[0].text) for res in results.generations]
        qas = [qa for resp in responses for qa in resp["questions"]]
        return {self.output_key: qas}
