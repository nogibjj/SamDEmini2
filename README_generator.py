import os
import subprocess

def get_env_info():
    # Get the current environment's installed packages
    result = subprocess.run(['pipreqs','--print'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def get_directory_structure():
    # Get the directory structure using the `tree` command
    try:
        result = subprocess.run(['tree', '.'], stdout=subprocess.PIPE)
        result = subprocess.run(['tree', '.', '-I', '__pycache__'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except FileNotFoundError:
        return "Please install 'tree' to display the directory structure."

def generate_readme():
    # Create README.md file and write environment and directory info
    with open('README.md', 'w') as readme_file:
        readme_file.write("# **The project is designed to illustrate a routine process of e-biz exploration**\n")


        readme_file.write("# \n\nUser Profile Explorision\n\n")
        readme_file.write("## Environment Information\n\n")
        readme_file.write("The project uses the following Python environment and dependencies:\n\n")
        readme_file.write("```\n")
        readme_file.write(get_env_info())
        readme_file.write("```\n\n")
        readme_file.write("## Project Structure\n\n")
        readme_file.write("Here is the structure of the project files and directories:\n\n")
        readme_file.write("```\n")
        readme_file.write(get_directory_structure())
        readme_file.write("```\n")
if __name__ == "__main__":
    generate_readme()
