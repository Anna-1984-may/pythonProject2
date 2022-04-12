from models import Project, Tag

current_tags = []

"""

def saver(name: str, tags: str) -> bool:
        tag1 = 0
        if name and tags:
            project_name = ProjectName.add(name)
            for tag in tags:
                ProjectTags.add(tags[tag1], project_name)
                tag1+=1
            return True
        return False
        
"""
def saver(name: str, tags: str) -> bool:
    if name and tags:
        project = Project.add(name)
        for tag in current_tags:
            Tag.add(tag, project)
        return True
    return False


