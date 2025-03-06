report_planner_query_writer_instructions = """You are performing research for a {document_type}. 

<Topic>
{topic}
</Topic>

<Organization>
{report_organization}
</Organization>

<Objective>
{objective}
</Objective>

<Task>
Your goal is to generate {number_of_queries} web search queries that will help gather information for planning the {document_type} sections. 

The queries should:

1. Be related to the main topic
2. Help satisfy the requirements specified in the organization
3. Find actionable, practical recommendations and implementation guidance
4. Uncover specific examples, case studies, and real-world applications
5. Target both foundational knowledge and cutting-edge developments
6. Include queries specifically for finding visual aids, code examples, or templates when relevant

Make the queries specific enough to find high-quality, relevant sources while covering the breadth needed for the structure.

For technical topics, include queries for code examples, implementation guides, and best practices.
For business or strategy topics, include queries for case studies, metrics, and benchmarks.
</Task>
"""

report_planner_instructions = """I want a plan for a {document_type} that is concise and focused on actionable insights with practical implementation guidance.

<Topic>
The topic is:
{topic}
</Topic>

<Organization>
This should follow this organization: 
{report_organization}
</Organization>

<Objective>
{objective}
</Objective>

<Context>
Here is context to use to plan the sections of the {document_type}: 
{context}
</Context>

<Task>
Generate a list of sections for the {document_type}. Your plan should be tight and focused with NO overlapping sections or unnecessary filler. 

The {document_type} should be focused on actionable insights with specific implementation steps and concrete examples.

For example, a good structure might look like:
1/ intro
2/ overview of topic A
3/ overview of topic B
4/ comparison between A and B with implementation guidance
5/ conclusion with actionable recommendations

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

query_writer_instructions = """You are an expert technical writer crafting targeted web search queries that will gather comprehensive information for writing a technical {document_type} section.

<Topic>
{topic}
</Topic>

<Section topic>
{section_topic}
</Section topic>

<Objective>
{objective}
</Objective>

<Task>
Your goal is to generate {number_of_queries} search queries that will help gather comprehensive information about the section topic. 

The queries should:

1. Be related to the topic 
2. Examine different aspects of the topic
3. Find specific examples, implementations, and case studies
4. Uncover actionable guidance and best practices
5. Target recent developments and cutting-edge approaches

Make the queries specific enough to find high-quality, relevant sources that provide practical, implementable information with concrete examples.
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
- Strict 150-200 word limit
- Use simple, clear language
- Use short paragraphs (2-3 sentences max)
- Use ## for section title (Markdown format)
- Include specific examples, code snippets, or case studies when relevant
- Focus on actionable insights and practical implementation
- For technical content, include working examples with proper explanation
- For business content, include real-world applications or case studies
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
4. Ensure the section includes practical, implementable insights
</Final Check>
"""

section_writer_inputs = """ 
<Topic>
{topic}
</Topic>

<Section name>
{section_name}
</Section name>

<Section topic>
{section_topic}
</Section topic>

<Objective>
{objective}
</Objective>

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

<Objective>
{objective}
</Objective>

<Task>
Evaluate whether the section content adequately addresses the section topic and provides actionable, practical insights.

Evaluation criteria:
1. Relevance to the section topic
2. Depth and comprehensiveness
3. Inclusion of specific examples or case studies
4. Actionable recommendations or implementation guidance
5. Clear, practical takeaways

If the section content does not adequately address the section topic or lacks practical examples and implementation guidance, generate {number_of_follow_up_queries} follow-up search queries to gather missing information.
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

<Objective>
{objective}
</Objective>

<Available content>
{context}
</Available content>

<Task>
1. Section-Specific Approach:

For Introduction:
- Use # for title (Markdown format)
- 50-100 word limit
- Write in simple and clear language
- Focus on the core motivation for the {document_type} in 1-2 paragraphs
- Use a clear narrative arc to introduce the topic
- Include NO structural elements (no lists or tables)
- No sources section needed

For Conclusion/Summary:
- Use ## for section title (Markdown format)
- 100-150 word limit
- For comparative topics:
    * Must include a focused comparison table using Markdown table syntax
    * Table should distill insights from the content
    * Keep table entries clear and concise
- For non-comparative topics: 
    * Only use ONE structural element IF it helps distill the points made:
    * Either a focused table comparing items present in the report (using Markdown table syntax)
    * Or a short list using proper Markdown list syntax:
      - Use `*` or `-` for unordered lists
      - Use `1.` for ordered lists
      - Ensure proper indentation and spacing
- End with specific next steps, actionable recommendations, or implementation guidance
- No sources section needed

3. Writing Approach:
- Use concrete details over general statements
- Make every word count
- Focus on your single most important point
- Include specific examples or implementations when relevant
- Ensure all recommendations are practical and actionable
</Task>

<Quality Checks>
- For introduction: 50-100 word limit, # for title, no structural elements, no sources section
- For conclusion: 100-150 word limit, ## for section title, only ONE structural element at most, no sources section
- Markdown format
- Clear, actionable recommendations
- Concrete examples or implementation guidance
- Do not include word count or any preamble in your response
</Quality Checks>"""
