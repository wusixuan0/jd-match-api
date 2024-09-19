from langchain_community.vectorstores import FAISS
from api.util.gemini_api_request import SimpleGeminiAPICall

def rag(question):
    vectorstore = load_faiss_index()
    retrieved_docs = retrieve(vectorstore, question)
    response = generate(retrieved_docs, question, model_name="gemini-1.5-pro-exp-0827")
    return response    

def generate(retrieved_docs, question, model_name):
    context = format_docs(retrieved_docs)
    prompt = rag_prompt(context, question)
    return SimpleGeminiAPICall(prompt, model_name)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)    

def retrieve(vectorstore, question):
    retrieved_docs = vectorstore.similarity_search(question)
    print(f"number of retrieved documents: {len(retrieved_docs)}")
    return retrieved_docs

def load_faiss_index():
    embeddings = get_embeddings()
    return FAISS.load_local(
    "faiss_index", embeddings, allow_dangerous_deserialization=True)

def pdf_to_vectorstore(file_path):
    splits = load_and_split(file_path)
    vectorstore = embed_and_store(splits)

def embed_and_store(splits):
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(splits, embeddings)
    vectorstore.save_local("faiss_index")
    return vectorstore

def get_embeddings():
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    import os
    if "GOOGLE_API_KEY" not in os.environ: raise ValueError("GOOGLE_API_KEY not set")
    
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def load_and_split(file_path):
    from langchain_community.document_loaders import PyMuPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=100)
    loader = PyMuPDFLoader(file_path)
    splits = loader.load_and_split(text_splitter)
    return splits

def load_pdf(file_path):
    from langchain_community.document_loaders import PyMuPDFLoader
    loader = PyMuPDFLoader(file_path)
    docs = loader.load()
    print(f"{len(docs)} pages")
    return docs

# def split(docs):
#     from langchain.text_splitter import RecursiveCharacterTextSplitter
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=100)
#     splits = text_splitter.split_documents(docs)
#     return splits

def rag_prompt(context, question):
    prompt = f"""
You're critical and harsh. You're not afraid to be offensive and discuss controvercial topics in radical feminism. you promote critical thinking.
Respond to the following question about "Beauty and Misogyny - Harmful Cultural Practices in the West" by Sheila Jeffreys. Analyze using the provided guideline, question analysis and context/relevant chapters from the book summaries to formulate your response. 
The guideline, relevant context from the book, and the question analysis are provided below, separated by XML tags.

<guideline>
Engaging question analysis with the text:
- Reflect on how these relate to the book's arguments.
- Locate relevant passages that address the question's key points.
- Critically examine the evidence Jeffreys uses to support her claims. Is it compelling? Why or why not?

Critical Thinking:

Analyze Jeffreys' arguments: What are the strengths and potential weaknesses?
Consider alternative perspectives: How might other scholars or cultural critics view this issue?
Reflect on potential biases: Both in Jeffreys' work and in your own interpretation.


Synthesizing Information:

Connect different parts of the book to form a comprehensive view of Jeffreys' stance.
Consider how Jeffreys' arguments relate to real-world practices and policies.
Explore potential implications of Jeffreys' ideas if applied in various cultural contexts.


Encouraging User Engagement:

Pose thought-provoking questions to the user that extend beyond the text.
Invite the user to consider how Jeffreys' arguments align or conflict with their own experiences or observations.
Suggest areas for further research or exploration related to the topic.


Acknowledging Limitations:

Be transparent about the limitations of the analysis based on the available context.
If a question cannot be confidently answered, explain why and suggest how one might go about finding the information.
Encourage skepticism and further investigation rather than presenting any interpretation as definitive.

Ethical Considerations:

Be mindful of the sensitive nature of the topics discussed. Provide content warnings when appropriate.
Strive for a balanced approach that respects diverse perspectives while critically examining harmful practices.
Encourage reflection on the ethical implications of beauty practices and cultural norms discussed in the book.

Copyright:
Avoid reproducing copyrighted material verbatim. Instead, summarize key points and use brief, attributed quotes if necessary.

Remember, the goal is not to provide a single "correct" answer, but to facilitate a deeper, more nuanced understanding of the text and its themes. Encourage both yourself and the user to question assumptions, consider multiple viewpoints, and engage in ongoing critical reflection.
</guideline>
<context>{context}</context>
<question>{question}</question>
    """
    return prompt

def question_analysis_prompt(question):
    return f"""
Critically analyze the question. a framework for rigorous question analysis is provided. you should adapt based on the specific context. Remember, this framework is not a checklist to be mindlessly followed. Each question requires a unique, thoughtful approach. Your analysis should demonstrate intellectual rigor, nuanced understanding, and engagement with diverse perspectives. Keep your response very concise but comprehensive.
<question>{question}</question>
<framework>
1. Deconstructing the Question:
  a) Identify key terms and concepts
  b) Examine implicit assumptions
  c) Consider the question's origin and potential biases
2. Main Topic Identification:
  a) Core issue(s) addressed
  b) Broader context and related themes
  c) Potential subtopics or nested issues
3. Theoretical Framework:
  a) Relevant academic disciplines
  b) Major theories applicable to the question
  c) Competing or contrasting theoretical approaches
  d) Historical development of pertinent theories
4. Assumptions Analysis:
  a) Explicit assumptions in the question
  b) Implicit assumptions (cultural, historical, ideological)
  c) Problematic assumptions:
    Overgeneralizations
    False dichotomies
    Ethnocentric or culturally biased views
    Ahistorical perspectives
  d) Correct or evidence-based assumptions
5. Contextual Considerations:
  a) Historical context
  b) Cultural context
  c) Socio-economic factors
  d) Power dynamics and intersectionality
Optional:
8. Critical Reflection:
  a) Limitations of the question itself
  b) Alternative framings or approaches
  c) Potential consequences or implications of the question
9. Ethical Considerations:
  a) Potential harm or benefit from pursuing this question
  b) Representation and voice - whose perspectives are centered/marginalized?
</framework>
"""

summrize_prompt = f"""Summarize the following chapter of the book while maintaining strict objectivity. 
Your task is to provide a comprehensive, concise and neutral summary of the book's content. In the summary, DO NOT expressing your own opinions or judgments.

**Focus on the following:**

<focus>

- **Main Arguments:** Clearly outline the author's central claims and supporting arguments and evidence. be comprehensive
- **Structure:** Structure the Arguments based on the book's organization and how the author develops their ideas.
- **Theoretical Framework:** Identify the key concepts, theories, or perspectives that inform the author's analysis.
- **Argumentative Style:** follow the author's typical methods of reasoning and persuasion.

</focus>

**Avoid:**

<avoid>

- Expressing your own opinions or beliefs about the book's content.
- Evaluating the validity or soundness of the author's arguments.
- Making subjective judgments about the author's style or intentions.

</avoid>

**Remember:**

<remember>

- Your goal is to present a factual and unbiased account of the book's contents, allowing readers to form their own interpretations.
- Use neutral language and avoid loaded terms that could convey bias.
- Include specific examples from the text to support your points.
- Write in your own words, be careful not to closely mirror the book's original language or structure.
Avoid reproducing copyrighted material verbatim. Instead, summarize key points and use brief, attributed quotes if necessary.

</remember>
"""
