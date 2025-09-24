from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from src.core.exceptions import ClientError
from src.core.weather_client import WeatherApiClient
from src.repository.message_repository import MessageRepository
from src.schema.message_schema import MessageCategory, MessageCreate
from src.services.base_service import BaseService


class MessageService(BaseService):
    def __init__(self, message_repository: MessageRepository, weather_client: WeatherApiClient):
        self.message_repository = message_repository
        self.weather_client = weather_client
        super().__init__(message_repository)

    async def create(self, schema: MessageCreate):
        # user_message = MessageCreate(content=schema.content, is_ai=False)
        # self.message_repository.create(user_message)
        template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a classifier. Read the following text and determine whether it is about food, weather, or none of the above.",
                ),
                (
                    "human",
                    "Text: {message}\nRespond only with one of these three labels: 'Food', 'Weather', or 'None'.",
                ),
            ]
        )

        # TODO: manage models in config
        llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0).with_structured_output(
            MessageCategory, method="json_schema"
        )

        chain = template | llm

        result = chain.invoke({"message": schema.content})

        if result.category == "None":
            raise ClientError(detail="Invalid message category")

        if result.category == "Food":
            search_results = self.message_repository.get_by_query(schema.content, k=3)
            # for i, result in enumerate(search_results, 1):
            #     print(f"Result {i}:")
            #     print(f"Source: {result.metadata.get('source', 'Unknown')}")
            #     print(f"Content: {result.page_content}")
            #     print()
            context = " ".join([doc.page_content for doc in search_results])
            prompt = ChatPromptTemplate.from_template(
                """You are a helpful assistant. 
                Use the provided context to answer the question.

                Context:
                {context}

                Question:
                {question}

                If the context does not contain the answer, say you don't know.
                """
            )
            llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0,
            )
            food_chain = prompt | llm | StrOutputParser()
            result = food_chain.invoke({"context": context, "question": schema.content})

            return self.message_repository.create(MessageCreate(content=result, is_ai=True))

        if result.category == "Weather":
            response = await self.weather_client.get_weather(location="New York")
            return self.message_repository.create(
                MessageCreate(
                    content=f"The current weather in New York is {response['current']['condition']['text']} with a temperature of {response['current']['temp_c']}°C.",
                    is_ai=False,
                )
            )
