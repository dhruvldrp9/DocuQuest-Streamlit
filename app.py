import streamlit as st
import os
from htmlTemplates import css, bot_template, user_template
from Parsers.zip_file_extractor import ZipFileExtractor
from Parsers.docx_parser import DocxParser
from Parsers.pdf_parser import PDFParser
from Parsers.pptx_parser import PPTXParser
from Parsers.link_parser import LinkParser
from AnswerGeneration.answer_generation import AnswerGeneration


def handle_userinput(user_question) :

    if st.session_state.conversation is None:
        st.error("Please upload a document or provide a URL before asking a question.")
        return

    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']


def show_chat_history() :

    for i, message in list(enumerate(st.session_state.chat_history)):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)




def main():
    raw_text = ""  # Initialize raw_text variable
    st.set_page_config(page_title="DocuQuest",)
    st.write(css, unsafe_allow_html=True)



    if 'conversation' not in st.session_state or st.session_state.conversation is None:
        st.session_state.conversation = None
    st.title("DocuQuest")
    if 'chat_history' not in st.session_state or st.session_state.chat_history is None:
        st.session_state.chat_history = []

    
    message = st.chat_input("Ask a question")

    handle_userinput(message)
    show_chat_history()

    with st.sidebar:
        st.title("DocuQuest")
        st.image('assets/DCUeest.jpeg')
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

        if openai_api_key == None:
            st.warning("Please enter your OpenAI API Key to proceed.")
            return
        st.subheader('supports only  PDF, DOCX, PPTX, ZIP and URL')

        docs = st.file_uploader("Upload a document", accept_multiple_files=True)
        url = st.text_input("Enter a URL")


        if st.button("Extract Data!"):
            with st.spinner("Doing RAG..."):
                if docs:
                    pdf_files = []
                    pptx_files = []
                    docx_files = []

                    for doc in docs:
                        if doc.name.endswith('.zip'):
                            ZipFileExtractor.unzip_file(doc, 'temp')

                            extracted_files = []
                            for root, dirs, files in os.walk('temp'):
                                for file in files:
                                    extracted_files.append(os.path.join(root, file))

                            print(f"Extracted files: {extracted_files}")
                            for file in extracted_files:
                                print(f"Processing file: {file}")
                                if file.endswith('.pdf'):
                                    pdf_files.append(file)
                                elif file.endswith('.docx'):
                                    docx_files.append(file)
                                elif file.endswith('.pptx'):
                                    pptx_files.append(file)
                        elif doc.name.endswith('.pdf'):
                            pdf_files.append(doc)
                        elif doc.name.endswith('.docx'):
                            docx_files.append(doc)
                        elif doc.name.endswith('.pptx'):
                            pptx_files.append(doc)

                    if pdf_files:
                        raw_text += PDFParser.get_pdf_text(pdf_files)
                    if docx_files:
                        for docx_file in docx_files:
                            raw_text += DocxParser.get_docx_text(docx_file)
                    if pptx_files:
                        raw_text += PPTXParser.get_pptx_text(pptx_files)

                    st.session_state.conversation = None  # Reset conversation

                elif url:
                    raw_text = LinkParser.get_website_text(url)
                    st.session_state.conversation = None  # Reset conversation

                else:
                    st.error("Please upload a supported file(s) or provide a URL for analysis.")
                    st.stop()

                if raw_text is None:
                    st.error("No text extracted from the documents.")
                    st.stop()
                try:
                    st.session_state.conversation = AnswerGeneration().get_answer(text=raw_text, openai_api_key=openai_api_key)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.stop()
                st.write("Text extraction completed! \n Ask a Query.")

        if st.button('Clear Data'):
        # Reset the FAISS database / vector store
            vector_store = None
            st.session_state.conversation = None
            st.session_state.chat_history = []
            st.write("Data has been cleared.")



if __name__ == '__main__':
    main()