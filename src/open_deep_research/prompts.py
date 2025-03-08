report_planner_query_writer_instructions = """You are performing background research to provide context for a {document_type}. 

<Report topic>
{topic}
</Report topic>

<Document-Organization>
{report_organization}
</Document-Organization>

<Document-Objective>
{objective}
</Document-Objective>

<Task>
Your goal is to generate {number_of_queries} web search queries that will help gather information for planning the {document_type} sections. 

The queries should:

1. Be related to the main topic
2. Help satisfy the requirements specified in the report organization
3. Find practical implementation guidance
4. Uncover specific examples, templates, tools, and real-world applications
5. Target both foundational knowledge and efficient implementation techniques

Make the queries specific enough to find high-quality, relevant sources while covering the breadth needed for the structure.

For technical topics, include queries for code examples, implementation guides, and step-by-step tutorials.
For practical topics, include queries for worked examples, resource collections, and implementation checklists.
</Task>
"""

report_planner_instructions = """I want a plan for a {document_type} that is concise and focused on actionable insights.

<Topic>
The topic is:
{topic}
</Topic>

<Document-Organization>
This should follow this organization: 
{report_organization}
</Document-Organization>

<Document-Objective>
{objective}
</Document-Objective>

<Context>
Here is context to use to plan the sections of the {document_type}: 
{context}
</Context>

<Task>
Generate a list of sections for the {document_type}. Your plan should be tight and focused with NO overlapping sections or unnecessary filler. 

The {document_type} should be focused on actionable insights with specific implementation steps and concrete examples.

For example, a good structure might look like:
1/ Overview & Objective
2/ Context & Background
3/ Implementation Approach
4/ Step-by-Step Implementation 
5/ Resources & Examples
6/ Evaluation & Next Steps

Each section should have the fields:

- Name - Name for this section of the {document_type}.
- Description - Brief overview of the main topics covered in this section.
- Research - Whether to perform web research for this section of the {document_type}.
- Content - The content of the section, which you will leave blank for now.

Integration guidelines:
- Include examples and implementation details within main topic sections, not as separate sections
- Ensure each section has a distinct purpose with no content overlap
- Combine related concepts rather than separating them
- For technical topics, ensure sections cover practical implementation, code examples, and best practices
- For business topics, ensure sections include case studies, practical applications, and metrics

Before submitting, review your structure to ensure it has no redundant sections and follows a logical flow.
</Task>

<Feedback>
Here is feedback on the structure from review (if any):
{feedback}
</Feedback>
"""

query_writer_instructions = """You are an expert technical writer crafting targeted web search queries that will gather comprehensive information for writing a {document_type} section.

<Topic>
{topic}
</Topic>

<Section topic>
{section_topic}
</Section topic>

<Document-Objective>
{objective}
</Document-Objective>

<Task>
Your goal is to generate {number_of_queries} search queries that will help gather comprehensive information about the section topic. 

The queries should:

1. Be related to the topic 
2. Examine different aspects of the topic with a focus on implementation
3. Find specific examples, templates, and step-by-step guides
4. Uncover practical resources and implementation best practices
5. Target efficient approaches and proven methodologies

Make the queries specific enough to find high-quality, relevant resources that provide detailed instructions, reusable tools, and practical examples that can be directly applied.
</Task>
"""

section_writer_instructions = """Write one section of a {document_type}.

<Task>
1. Review the topic, section name, and section topic carefully.
2. If present, review any existing section content. 
3. Then, look at the provided Source material.
4. Decide the sources that you will use to write this section.
5. Write the section and list your sources. 
</Task>

<Writing Guidelines>
- If existing section content is not populated, write from scratch
- If existing section content is populated, synthesize it with the source material
- Important: do not add preamble. Begin exactly with the section title.
- Keep it to a 300 word limit unless there is a good reason to exceed it
- Use simple, clear language optimized for implementation
- Use short paragraphs (2-3 sentences max)
- Use ## for section title (Markdown format)
- Include specific examples, code snippets, templates, or step-by-step procedures when relevant
- Focus on detailed implementation guidance with concrete steps
- For technical content, include working examples with clear instructions
- For practical content, include resource links and implementation checklists when possible
</Writing Guidelines>

<Citation Rules>
- Assign each unique URL a single citation number in your text
- End with ### Sources that lists each source with corresponding numbers
- IMPORTANT: Number sources sequentially without gaps (1,2,3,4...) in the final list regardless of which sources you choose
- Example format:
  [1] Source Title: URL
  [2] Source Title: URL
</Citation Rules>

<Final Check>
1. Verify that EVERY claim is grounded in the provided Source material
2. Confirm each URL appears ONLY ONCE in the Source list
3. Verify that sources are numbered sequentially (1,2,3...) without any gaps
4. Ensure the section includes clear, specific implementation guidance
</Final Check>
"""

section_writer_inputs = """ 

<Document-Type>
{document_type}
</Document-Type>

<Topic>
{topic}
</Topic>

<Section name>
{section_name}
</Section name>

<Section topic>
{section_topic}
</Section topic>

<Existing section content (if populated)>
{section_content}
</Existing section content>

<Source material>
{context}
</Source material>
"""

section_grader_instructions = """Review a {document_type} section relative to the specified topic:

<Topic>
{topic}
</Topic>

<Section topic>
{section_topic}
</Section topic>

<Section content>
{section}
</Section content>

<Document-Objective>
{objective}
</Document-Objective>

<Task>
Evaluate whether the section content adequately addresses the section topic and provides detailed, step-by-step implementation guidance.

Evaluation criteria:
1. Relevance to the section topic
2. Clarity and specificity of instructions
3. Inclusion of practical examples, templates, or resources
4. Step-by-step implementation guidance
5. Useful tactics and implementation tips

If the section content does not adequately address the section topic or lacks detailed implementation guidance, generate {number_of_follow_up_queries} follow-up search queries to gather missing information.
</Task>

<Format>
    grade: Literal["pass","fail"] = Field(
        description="Evaluation result indicating whether the response meets requirements ('pass') or needs revision ('fail')."
    )
    follow_up_queries: List[SearchQuery] = Field(
        description="List of follow-up search queries.",
    )
</Format>
"""

final_section_writer_instructions = """You are an expert technical writer crafting a section that synthesizes information from the rest of the {document_type}.

<Topic>
{topic}
</Topic>

<Section name>
{section_name}
</Section name>

<Section topic> 
{section_topic}
</Section topic>

<Document-Objective>
{objective}
</Document-Objective>

<Available content>
{context}
</Available content>

<Task>
1. Section-Specific Approach:

For Introduction:
- Use # for title (Markdown format)
- 200 word limit
- Write in simple, clear language
- Highlight what the reader will be able to accomplish with these instructions and how they should be able to use it.
- Include NO structural elements (no lists or tables)
- No sources section needed

For Conclusion/Summary:
- Use ## for section title (Markdown format)
- 300 word limit
- For technical implementation topics:
    * Include a focused implementation checklist or key steps summary using Markdown list syntax
    * Highlight critical resources or tools mentioned in the guide
- For process-oriented topics: 
    * Only use ONE structural element that helps consolidate the guidance:
    * Either a focused checklist of implementation steps (using Markdown list syntax)
    * Or a quick-reference table of resources/tools with their purposes (using Markdown table syntax)
    * Ensure proper indentation and spacing
- End with clear next steps or immediate actions the reader can take
- No sources section needed

3. Writing Approach:
- Focus on practical, immediately applicable guidance
- Emphasize concrete steps over theoretical concepts
- Reference specific resources, templates, and tools when available
- Ensure all instructions are clear and actionable
- Include troubleshooting tips or common pitfalls where relevant
</Task>

<Quality Checks>
- For introduction: 200 word limit, # for title, no structural elements, no sources section
- For conclusion: 300 word limit, ## for section title, only ONE structural element at most, no sources section
- Markdown format
- Clear, step-by-step instructions
- Specific resources or implementation tools
- Do not include word count or any preamble in your response
- Important: Output only the section content, no other text (i.e. no "Here is the section...", no "I'll review and enhance the existing section..." or anything like that)
</Quality Checks>"""
