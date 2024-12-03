import os
import hashlib
import time

class SimpleGit:
    def __init__(self, repo_name):
        self.repo_name = repo_name  # Name of the repository
        self.repo_dir = f"./{repo_name}/.mygit"  # Directory where the repo data is stored
        self.staging_area = f"./{repo_name}/staging"  # Temporary area to stage files before committing
        self.commits = []  # To store commit history
        os.makedirs(self.repo_dir, exist_ok=True)  # Create .mygit folder if not exist
        os.makedirs(self.staging_area, exist_ok=True)  # Create staging area

    def init(self):
        """Initializes the repository (creates the .mygit folder)."""
        if not os.path.exists(self.repo_dir):
            os.makedirs(self.repo_dir)
            with open(f"{self.repo_dir}/HEAD", "w") as head_file:
                head_file.write("master\n")  # Point to the main branch (master)
            print(f"Initialized empty repository in {self.repo_name}")

    def stage(self, filename):
        """Stages a file (like git add)."""
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                content = file.read()
                file_hash = hashlib.sha1(content.encode()).hexdigest()  # Hash the file content
                staged_file = os.path.join(self.staging_area, f"{file_hash}_{filename}")
                with open(staged_file, "w") as staged:
                    staged.write(content)  # Save the file in staging area
                print(f"Staged file: {filename}")
        else:
            print(f"{filename} not found!")

    def commit(self, message):
        """Commits the staged files (like git commit)."""
        staged_files = os.listdir(self.staging_area)  # Get all staged files
        if staged_files:
            commit_hash = hashlib.sha1(message.encode() + str(time.time()).encode()).hexdigest()  # Generate a commit hash
            commit = {
                'hash': commit_hash,
                'message': message,
                'files': staged_files,
                'time': time.time()
            }
            self.commits.append(commit)  # Add commit to history
            # Clear the staging area after commit
            for file in staged_files:
                os.remove(os.path.join(self.staging_area, file))
            print(f"Committed: {message}")
        else:
            print("No files staged to commit!")

    def show_commit_history(self):
        """Shows the commit history."""
        if not self.commits:
            print("No commits found!")
            return
        for commit in self.commits:
            print(f"Commit {commit['hash'][:7]}: {commit['message']}")
            print(f"Files: {commit['files']}")
            print(f"Time: {time.ctime(commit['time'])}")
            print("-" * 40)

# Example usage:
repo = SimpleGit("myrepo")  # Create a new repo named "myrepo"
repo.init()  # Initialize the repository
repo.stage("file1.txt")  # Stage file1.txt
repo.commit("Initial commit")  # Commit with a message
repo.show_commit_history()  # Show commit history
