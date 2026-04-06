# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: [Pham Viet Anh]
- **Student ID**: [2A202600273]
- **Date**: [4/6/2026]

---

## I. Technical Contribution (15 Points)

*Describe your specific contribution to the codebase (e.g., implemented a specific tool, fixed the parser, etc.).*

- **Modules Implementated**: src/agents/agent.py
- **Code Highlights**: 

def run(self, user_input: str) -> str:
    # Initialize the conversation context with the user's request
    current_prompt = f"User Request: {user_input}\nBegin reasoning."
    steps = 0

    while steps < self.max_steps:
        # 1. Generate Thought and Action from the LLM
        response = self.llm.generate(current_prompt, system_prompt=self.get_system_prompt())
        
        # 2. Check for the Stop Condition (Final Answer)
        if "Final Answer:" in response:
            return response.split("Final Answer:")[-1].strip()

        # 3. Parse the Action using Regex to extract tool_name and arguments
        action_match = re.search(r"Action:\s*(\w+)\((.*)\)", response)
        if action_match:
            tool_name = action_match.group(1)
            tool_args = action_match.group(2)
            
            # 4. Execute the identified tool and retrieve the Observation
            observation = self._execute_tool(tool_name, tool_args)
            
            # 5. Append the Thought, Action, and Observation back to the prompt for the next iteration
            current_prompt += f"\n{response}\nObservation: {observation}"
        
        steps += 1
    
    return "Agent stopped: reached maximum iterations without a final answer."
- **Documentation**: 
My code interacts with the ReAct loop by managing a continuous cycle of five distinct stages 
Reasoning (Thought): The Agent uses the LLM to analyze the current state and determine what information or action is missing.
Action Selection: Based on the reasoning, the Agent selects a specific tool (e.g., evaluate_submission or search_flights) and defines the necessary parameters.
Tool Execution: The run method parses the LLM's text output into executable Python commands to interact with external APIs or local databases.
Observation Acquisition: The result from the tool execution is captured as an "Observation," providing real-world data back to the Agent.
Context Integration: The Observation is fed back into the prompt, allowing the Agent to "remember" previous steps and adjust its next Thought accordingly (e.g., deciding to PASS a student only after verifying both their score and study time)

---

## II. Debugging Case Study (10 Points)

*Analyze a specific failure event you encountered during the lab using the logging system.*

- **Problem Description**: The Agent entered an infinite loop where it repeatedly called the same tool with identical parameters (e.g., Action: check_weather('Da Nang')) despite already receiving the observation
- **Diagnosis**: The LLM failed to acknowledge the existing Observation in the history. This happened because the current_prompt update logic in the run method did not clearly distinguish between new instructions and previous results, causing the model to lose track of its progress.
- **Solution**: I updated the run method to explicitly label the history and modified the System Prompt to include a rule: "Never call the same tool twice with the same arguments. If you have the Observation, proceed to the next Thought"

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

*Reflect on the reasoning capability difference.*

1.  **Reasoning**: The Thought block acts as a "scratchpad" for the Agent. Unlike a standard Chatbot that jumps directly to an answer (often hallucinating facts), the Thought block forces the Agent to decompose a complex goal into smaller, logical sub-tasks, such as "First check the score, then check the study time".
2.  **Reliability**: The Agent actually performed worse than a standard Chatbot in low-complexity tasks where a direct answer was available in the LLM's training data. For simple "Hello" or "Tell me a joke" prompts, the ReAct overhead (Thinking/Action steps) increased latency and occasionally led the Agent to try and "find a tool" for a task that didn't require one.
3.  **Observation**: Environment feedback (Observations) served as a "reality check". For example, if evaluate_submission returned a low score (e.g., score = 5), the Observation immediately shifted the Agent's next Thought from "Everything looks good" to "The student failed the criteria; I must now analyze the errors".

---

## IV. Future Improvements (5 Points)

*How would you scale this for a production-level AI agent system?*

- **Scalability**: Implement an Asynchronous Task Queue (e.g., using Celery or Redis) for tool calls. This would allow the Agent to handle long-running tool executions (like complex web scraping) without blocking the main event loop, enabling multiple agents to run concurrently.
- **Safety**: or "Human-in-the-loop" gatekeeper. For sensitive actions like execute_decision(FAIL), a production system should require an audit by a second, more restricted LLM to ensure the Agent's reasoning aligns with institutional policies.
- **Performance**: Use a Vector Database (e.g., Pinecone or Weaviate) for Tool Retrieval. As the number of available tools grows, instead of stuffing all tool descriptions into the System Prompt (which wastes tokens and causes noise), the system could dynamically retrieve only the top 3-5 most relevant tools based on the current user intent

---

> [!NOTE]
> Submit this report by renaming it to `REPORT_[YOUR_NAME].md` and placing it in this folder.
