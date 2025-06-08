import os
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temprature=0, groq_api_key = os.getenv("GROQ_API_KEY"), model="groq/groq-llama-3-70b-instruct")

    def extract_jobs(self, input_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEB PAGE:
            {page_data}
            ### TASK:
            The scraped text above is from a job posting. Extract the following information in JSON format containing the keys:
            'role', 'experience', 'skills', 'description'.
            Only return the valid JSOn.kwargs=## Valid JSON (NO PREAMBLE):
            """
    )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": input_text})
        try:
            json_parse = JsonOutputParser()
            res = json_parse.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Failed to parse the output. Please ensure the output is in valid JSON format.")
        return res if isinstance(res, list) else {res}
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(input=input_text)
    def write_mail(self, job, links):
        prompt_mail = PromptTemplate.from_template(
            """
            ### JOB DETAILS:
            {job}
            ### LINKS:
            {links}
            ### TASK:
            Write a cold email to the hiring manager of the company with the job details provided above.
            The email should be professional, concise, and express interest in the job position.
            """
        )
        chain_email = prompt_mail | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res
if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))