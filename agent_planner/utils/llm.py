from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq()


def chat_model(
    model: str,
    msg: list,
    tools: list = None,
    temperature: float = 1.0,
    tool_choice: str = "auto",
):
    completion = client.chat.completions.create(
        model=model,
        messages=msg,
        temperature=temperature,
        max_completion_tokens=2048,
        top_p=1,
        tools=tools,
        tool_choice=tool_choice,
        stop=None,
    )

    return completion


def execute_tool_call(tool_call):
    """Parse and execute a single tool call"""
    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(tool_call.function.arguments)
    return function_to_call(**function_args)


available_functions = {}

if __name__ == "__main__":
    messages = [{"role": "user", "content": "What is the weather in india"}]

    response = chat_model("openai/gpt-oss-20b", messages)
    messages.append(response.choices[0].message)

    print(f"{messages[-1].role}:{messages[-1].content}")

    if response.choices[0].message.tool_calls:
        print("tool called\n\n")
        for tool_call in response.choices[0].message.tool_calls:
            function_response = execute_tool_call(tool_call)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": str(function_response),
                }
            )

    final = client.chat.completions.create(
        model="openai/gpt-oss-20b", messages=messages
    )

    print(final.choices[0].message.content.strip())
