from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
import json

# Load the OpenAI API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

def generate_lesson(topic: str, level: str = "Beginner", preference: str = "Theoretical"):
    """
    Generates a structured lesson on a given topic, tailored to the learner's level and preference.

    Args:
        topic (str): The topic of the lesson.
        level (str): The learner's level (e.g., Beginner, Intermediate, Advanced).
        preference (str): The learner's preference (e.g., Theoretical, Practical).

    Returns:
        dict: A dictionary containing the lesson content. If the response is valid JSON, it is parsed.
              Otherwise, the content is returned as plain text under the key "lesson_content".
    """
    # Initialize the ChatOpenAI client
    llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0.7)

    # Define the prompt template
    prompt = PromptTemplate(
        input_variables=["topic", "level", "preference"],
        template="""
        Generate a comprehensive, engaging, and structured lesson about **{topic}** tailored for a **{level}** learner. The lesson should align with the learner's **{preference}** (e.g., theoretical, practical, visual, or hands-on). Ensure the lesson is clear, concise, and accessible, while also being detailed enough to foster deep understanding.

        The lesson must include the following sections, formatted in markdown for readability:

        ### 1. **Introduction**
           - Provide a **brief overview** of the topic, its significance, and its real-world applications.
           - Explain **why this topic is important** for learners at the **{level}** level.
           - Include a **motivational hook** to engage the learner and spark curiosity about the topic.
           - If applicable, provide a **historical context** or evolution of the topic to give the learner a broader perspective.

        ### 2. **Learning Objectives**
           - Clearly list **3-5 specific learning objectives** that the lesson will cover.
           - Ensure these objectives are measurable and aligned with the learner's **{level}** and **{preference}**.
           - Example: "By the end of this lesson, you will be able to: [...]"

        ### 3. **Key Concepts**
           - Break down the topic into **logical subtopics** or core ideas.
           - For each subtopic:
             - Provide a **clear and concise explanation** using language appropriate for the learner's **{level}**.
             - Use **examples**, **analogies**, and **visual aids** (e.g., diagrams, charts, or graphs) to enhance understanding.
             - Highlight **connections** between subtopics to show how they relate to each other.
           - If the topic involves technical or abstract concepts, include **mnemonics** or **memory aids** to help the learner retain information.

        ### 4. **Practical Application**
           - Demonstrate how the topic can be applied in **real-world scenarios** or practical situations.
           - Include **case studies**, **code snippets**, or **step-by-step tutorials** for hands-on learners.
           - For visual learners, provide **diagrams**, **flowcharts**, or **infographics** to illustrate concepts.
           - For practical learners, include **interactive exercises** or **simulations**.

        ### 5. **Common Mistakes and Misconceptions**
           - Identify **3-5 common mistakes** or misconceptions learners often encounter when studying this topic.
           - Explain **why these mistakes occur** and how to **avoid or correct them**.
           - Provide **tips** or **best practices** to help the learner navigate potential challenges.

        ### 6. **Exercises and Activities**
           - Design **2-3 exercises** or activities to reinforce the learner's understanding of the topic.
           - Tailor the exercises to the learner's **{preference}**:
             - For **theoretical learners**: Include conceptual questions, essay prompts, or critical thinking challenges.
             - For **practical learners**: Provide coding challenges, real-world problem-solving tasks, or hands-on projects.
           - Include **solutions** or **answer keys** with detailed explanations to help the learner self-assess.

        ### 7. **Advanced Exploration (Optional)**
           - Suggest **additional resources** (e.g., books, articles, videos, or online courses) for learners who want to dive deeper into the topic.
           - Provide **challenge questions** or **advanced exercises** for learners who want to test their knowledge further.
           - Highlight **emerging trends** or **future directions** related to the topic to inspire curiosity.

        ### 8. **Summary and Key Takeaways**
           - Summarize the **main points** of the lesson in **bullet points** for quick review.
           - Reiterate the **learning objectives** and how they were addressed in the lesson.
           - End with a **motivational note** to encourage the learner to continue exploring the topic and applying their knowledge.

        ### 9. **Feedback and Reflection**
           - Include a **self-reflection prompt** to help the learner assess their understanding of the topic.
           - Example: "What was the most challenging part of this lesson for you? How can you apply what you've learned in your own context?"
           - Encourage the learner to provide feedback on the lesson to improve future iterations.

        ### Formatting Guidelines:
           - Use **markdown** for headings, bullet points, and code blocks.
           - Ensure the lesson is **visually appealing** with proper spacing, bold text for emphasis, and clear section divisions.
           - Use **simple language** for beginners, **technical terms** for advanced learners, and **explanations** for intermediate learners.

        ### Additional Notes:
           - Adapt the tone and depth of the lesson to the learner's **{level}** (e.g., beginner, intermediate, advanced).
           - Ensure the lesson is **inclusive** and accessible to learners with diverse backgrounds.
           - Use **active voice** and **engaging language** to maintain the learner's interest throughout the lesson.
        """
    )

    # Create the chain
    chain = prompt | llm

    try:
        # Run the chain and get the response
        response = chain.invoke({"topic": topic, "level": level, "preference": preference})

        # Attempt to parse the response as JSON
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            # If parsing fails, return the response as plain text
            return {"lesson_content": response.content}

    except Exception as e:
        raise RuntimeError(f"Failed to generate lesson: {str(e)}")

# Example usage
if __name__ == "__main__":
    topic = "machine learning"
    level = "beginner"
    preference = "theoretical"

    try:
        lesson = generate_lesson(topic, level, preference)
        print(json.dumps(lesson, indent=4))  # Pretty-print the output
    except Exception as e:
        print(f"Error: {e}")