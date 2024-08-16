from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from api.util.send_log import send_log
import time
from datetime import datetime

def semantic_search(jd_by_id_dict, resume_summary):
    start_time_datetime = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
    send_log(f">>>Starting Semantic Search  {start_time_datetime}")
    es_retrieve_result_toekn_size = len(str(jd_by_id_dict))
    es_retrieve_result_num = len(jd_by_id_dict)
    send_log(f"OpenSearch retrieved JDs have: {es_retrieve_result_toekn_size} characters")
    send_log(f"OpenSearch retrieved {es_retrieve_result_num} documents of job description")
    send_log(f"Average job description has {es_retrieve_result_toekn_size/es_retrieve_result_num} characters")
    
    jd_splits = split(jd_by_id_dict)
    vectorstore = embed(jd_splits)

    similar_by_field = retrieve_from_vectorstore(vectorstore, resume_summary, len(jd_splits))
    fused_score_by_id = weighted_reciprocal_rank_fusion(similar_by_field)
    ranked_fused_score_by_id = dict(sorted(fused_score_by_id.items(), key = lambda x: x[1], reverse = True))
    send_log(f"fused score {ranked_fused_score_by_id}")
    # send_log(f"num of jd from semantic search: {len(ranked_fused_score_by_id)}")

    filtered_jd_by_id_dict = filter_dictionary_by_ranked_ids(jd_by_id_dict, ranked_fused_score_by_id.keys())
    
    send_log(f"<<<Finished Semantic Search. Number of job descriptions is filtered down to: \n{len(filtered_jd_by_id_dict)}")
    return filtered_jd_by_id_dict

def weighted_reciprocal_rank_fusion(similar_by_field, k=60):
    fused_scores = {}
    weights = {
        "qualifications": 0.9,
        "preferences": 0.1,
    }
    for field in similar_by_field:
        field_weight = weights.get(field)
        docs_each_field = similar_by_field[field]
        for rank, doc in enumerate(docs_each_field):
            id = doc.metadata['jd_id']
            if id not in fused_scores:
                fused_scores[id] = 0
            fused_scores[id] += field_weight * (1 / (rank + k))
    return fused_scores

def retrieve_from_vectorstore(vectorstore, resume_summary, k):
    similar_by_field = {}
    qualifications=f"{resume_summary.get('skills')} {resume_summary.get('qualifications')}"
    num_chunks = vectorstore.index.ntotal
    send_log(f"Number of chunks in Faiss vectorstore: {num_chunks} calculated by faiss_vectorstore.index.ntotal")
   
    if resume_summary.get('qualifications'):
        similar_by_field['qualifications'] = vectorstore.similarity_search(qualifications, min(num_chunks,k))
    if resume_summary.get('preferences'):
        similar_by_field['preferences'] = vectorstore.similarity_search(resume_summary.get('preferences'), min(num_chunks,k))
    return similar_by_field

def embed(splits):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(splits, embeddings)
    return vectorstore

def split(jd_by_id_dict):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    jd_docs = [Document(page_content=text, metadata={"jd_id": id}) for id, text in jd_by_id_dict.items()]
    jd_splits = text_splitter.split_documents(jd_docs)
    send_log(f"Number of splitted JD chunks: {len(jd_splits)}")
    return jd_splits


def filter_dictionary_by_ranked_ids(id_description_dict, ranked_ids):
    """
    Filters the dictionary to return only the key-value pairs where the key is in the ranked_ids list.

    Parameters:
    - id_description_dict (dict): A dictionary where keys are IDs and values are descriptions.
    - ranked_ids (list): A list of IDs in the desired order.

    Returns:
    - dict: A filtered dictionary with only the keys present in ranked_ids, in the order they appear in ranked_ids.
    """
    return {id_: id_description_dict[id_] for id_ in ranked_ids if id_ in id_description_dict}