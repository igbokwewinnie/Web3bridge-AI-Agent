import io
import zipfile
import requests
import frontmatter
from minsearch import Index


def safe_load_frontmatter(content: str):
    """Safely load Markdown frontmatter, fallback to raw text if invalid."""
    try:
        post = frontmatter.loads(content)
        data = post.to_dict()
        # Ensure 'content' key exists
        if 'content' not in data:
            data['content'] = post.content
        return data
    except Exception:
        # If file doesn't have valid frontmatter, return plain content
        return {"content": content}


def read_repo_data(repo_owner, repo_name):
    """Downloads and extracts markdown files from a GitHub repo."""
    url = f'https://codeload.github.com/{repo_owner}/{repo_name}/zip/refs/heads/main'
    print(f"📦 Downloading repository: {url}")

    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f"❌ Failed to download repo: {resp.status_code}")

    repository_data = []
    zf = zipfile.ZipFile(io.BytesIO(resp.content))

    for file_info in zf.infolist():
        filename = file_info.filename.lower()

        # Only load markdown files
        if not (filename.endswith('.md') or filename.endswith('.mdx')):
            continue

        with zf.open(file_info) as f_in:
            content = f_in.read().decode("utf-8", errors="ignore")
            data = safe_load_frontmatter(content)

            # Clean file path for readability
            _, filename_repo = file_info.filename.split('/', maxsplit=1)
            data['filename'] = filename_repo
            repository_data.append(data)

    zf.close()
    print(f"✅ Loaded {len(repository_data)} markdown files.")
    return repository_data


def sliding_window(seq, size, step):
    """Splits text into overlapping windows (chunks)."""
    if size <= 0 or step <= 0:
        raise ValueError("size and step must be positive")

    n = len(seq)
    result = []
    for i in range(0, n, step):
        batch = seq[i:i + size]
        result.append({'start': i, 'content': batch})
        if i + size > n:
            break
    return result


def chunk_documents(docs, size=2000, step=1000):
    """Applies sliding window chunking to all docs."""
    chunks = []

    for doc in docs:
        doc_copy = doc.copy()
        doc_content = doc_copy.pop('content', '')
        doc_chunks = sliding_window(doc_content, size=size, step=step)
        for chunk in doc_chunks:
            chunk.update(doc_copy)
        chunks.extend(doc_chunks)

    print(f"🧩 Created {len(chunks)} chunks from {len(docs)} documents.")
    return chunks


def index_data(repo_owner, repo_name, filter=None, chunk=False, chunking_params=None):
    """Runs the full ingestion pipeline: load → filter → chunk → index."""
    docs = read_repo_data(repo_owner, repo_name)

    # Optional filtering
    if filter is not None:
        docs = [doc for doc in docs if filter(doc)]

    # Optional chunking
    if chunk:
        if chunking_params is None:
            chunking_params = {'size': 2000, 'step': 1000}
        docs = chunk_documents(docs, **chunking_params)

    index = Index(text_fields=["content", "filename"])
    index.fit(docs)
    print("✅ Index built successfully!")
    return index
