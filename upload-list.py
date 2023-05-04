from todoist_api_python.api import TodoistAPI

with open('shoppingList.txt', 'r') as f:
    text = f.read()

text = text.split("\n")
text = text[2:]
section_bool = True
section_dict = {}
section = ''
for line in text:
    if line == '':
        section_bool = not section_bool
        continue

    if section_bool:
        section = line
        section_dict[section] = []
    else:
        section_dict[section].append(line)

project_name = "Shopping List"
list_project = None
with open('token.txt', 'r') as f:
    token = f.read()
api = TodoistAPI(token.strip())

try:
    projects = api.get_projects()
    for project in projects:
        if project.name == project_name:
            list_project = project
except Exception as error:
    print(error)

try:
    sections = api.get_sections(project_id=list_project.id)
    todoist_section_dict = {section.name: section for section in sections}
    todoist_section_name_list = list(todoist_section_dict.keys())

    for section_name in section_dict.keys():
        if section_name not in todoist_section_name_list:
            try:
                section = api.add_section(name=section_name, project_id=list_project.id)
                todoist_section_dict[section.name] = section
            except Exception as error:
                print(error)
except Exception as error:
    print(error)


for section, item_list in section_dict.items():
    for item in item_list:
        try:
            task = api.add_task(
                content=item,
                project_id=list_project.id,
                section_id=todoist_section_dict[section].id
            )
        except Exception as error:
            print(error)
