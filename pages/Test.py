import streamlit as st
import requests
import base64
from urllib.parse import urlparse

# Function to get repository information
def get_repo_info(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

# Function to get repository contents
def get_repo_contents(owner, repo, path=""):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

# Function to get README content
def get_readme_content(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    response = requests.get(url)
    if response.status_code == 200:
        content = response.json()["content"]
        return base64.b64decode(content).decode("utf-8")
    return None

# Streamlit app
st.title("GitHub Project Highlights")

# User input for GitHub repository URL
repo_url = st.text_input("Enter GitHub repository URL:")

if repo_url:
    # Parse the URL to extract owner and repo name
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip("/").split("/")
    
    if len(path_parts) >= 2:
        owner, repo = path_parts[:2]
        
        # Fetch repository information
        repo_info = get_repo_info(owner, repo)
        
        if repo_info:
            st.header(f"Repository: {repo_info['full_name']}")
            
            # Display repository stats
            col1, col2, col3 = st.columns(3)
            col1.metric("Stars", repo_info["stargazers_count"])
            col2.metric("Forks", repo_info["forks_count"])
            col3.metric("Open Issues", repo_info["open_issues_count"])
            
            # Display repository description
            st.subheader("Description")
            st.write(repo_info["description"])
            
            # Display most recently updated files
            st.subheader("Recently Updated Files")
            contents = get_repo_contents(owner, repo)
            if contents:
            # Sort by 'updated_at' if it exists, else default to an empty string for items without it
            sorted_contents = sorted(contents, key=lambda x: x.get("updated_at", ""), reverse=True)
            for item in sorted_contents[:5]:
            # Check if 'updated_at' exists in the item
            updated_at = item.get("updated_at", "N/A")  # Default to "N/A" if 'updated_at' is not available
            st.write(f"- {item['name']} (Last updated: {updated_at})")
            
            # Display README content
            st.subheader("README")
            readme_content = get_readme_content(owner, repo)
            if readme_content:
                st.markdown(readme_content)
            else:
                st.write("No README found in the repository.")
        else:
            st.error("Unable to fetch repository information. Please check the URL and try again.")
    else:
        st.error("Invalid GitHub repository URL. Please enter a valid URL.")

st.sidebar.markdown("""
## How to use
1. Enter a valid GitHub repository URL in the text box.
2. The app will display key information about the repository, including:
   - Repository stats (stars, forks, open issues)
   - Description
   - Recently updated files
   - README content
""")
