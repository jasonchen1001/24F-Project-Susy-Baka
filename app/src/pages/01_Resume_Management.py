import streamlit as st
import requests

# 确保用户已登录并具有学生角色
if st.session_state.get('authenticated', False) and st.session_state.get('role') == 'Student':
    st.title("Resume Management")

    # 查看简历列表
    if st.button("View Resumes"):
        response = requests.get("http://localhost:5000/resumes")
        if response.status_code == 200:
            resumes = response.json()
            if resumes:
                st.table(resumes)
            else:
                st.info("No resumes found.")
        else:
            st.error("Failed to fetch resumes.")

    # 上传新简历
    st.subheader("Upload a New Resume")
    resume_id = st.text_input("Resume ID")
    doc_name = st.text_input("Document Name")
    uploaded_file = st.file_uploader("Upload Resume File (PDF/Word)", type=["pdf", "docx"])

    if st.button("Upload Resume"):
        if uploaded_file and resume_id and doc_name:
            files = {"file": uploaded_file.getvalue()}
            data = {"resume_id": resume_id, "user_id": st.session_state.get('user_id'), "doc_name": doc_name}
            response = requests.post("http://localhost:5000/resumes", json=data)
            if response.status_code == 201:
                st.success("Resume uploaded successfully!")
            else:
                st.error(f"Failed to upload resume. Error: {response.text}")
        else:
            st.warning("Please fill in all fields and upload a file before submitting.")

    # 更新简历信息
    st.subheader("Update Resume")
    update_resume_id = st.text_input("Resume ID to Update")
    new_doc_name = st.text_input("New Document Name")

    if st.button("Update Resume"):
        if update_resume_id and new_doc_name:
            response = requests.put(f"http://localhost:5000/resumes/{update_resume_id}", json={"doc_name": new_doc_name})
            if response.status_code == 200:
                st.success("Resume updated successfully!")
            else:
                st.error(f"Failed to update resume. Error: {response.text}")
        else:
            st.warning("Please fill in all fields before submitting.")

    # 删除简历
    st.subheader("Delete Resume")
    delete_resume_id = st.text_input("Resume ID to Delete")

    if st.button("Delete Resume"):
        if delete_resume_id:
            response = requests.delete(f"http://localhost:5000/resumes/{delete_resume_id}")
            if response.status_code == 200:
                st.success("Resume deleted successfully!")
            else:
                st.error(f"Failed to delete resume. Error: {response.text}")
        else:
            st.warning("Please enter a Resume ID to delete.")

else:
    st.error("You are not authorized to view this page.")
